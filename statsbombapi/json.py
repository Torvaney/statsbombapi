import collections.abc
import datetime
import enum
import marshmallow
import typing
import uuid

import dataclasses
import dataclasses_json


def json_prefix(prefix, include=None, exclude=None):
    """ Add a json prefix to any dataclass attributes that do not have field information set. """
    def process(cls):
        attr_names = include or cls.__dict__.get('__annotations__', {})
        for a_name in attr_names:
            if a_name in (exclude or []):
                continue

            a_value = getattr(cls, a_name, dataclasses.MISSING)
            if isinstance(a_value, dataclasses.Field):
                # TODO: in the case that a Field is already set, consider *merging* instead of simply
                # skipping
                continue

            prefixed_field = dataclasses.field(
                default=a_value,
                metadata=dataclasses_json.config(field_name=prefix + a_name)
            )
            setattr(cls, a_name, prefixed_field)
        return cls
    return process


def add_prefix(d: typing.Dict[str, typing.Any], prefix: str) -> typing.Dict[str, typing.Any]:
    """ Add a prefix to the keys of a dict. """
    return {prefix + k: v for k, v in d.items()}


def remove_prefix(d: typing.Dict[str, typing.Any], prefix: str) -> typing.Dict[str, typing.Any]:
    """ Remove a prefix from the keys of a dict. """
    return {k.lstrip(prefix): v for k, v in d.items()}


def with_prefix(x, prefix):
    """ Add a prefix to a dataclass_json's encoder/decoder """
    return dataclasses.field(metadata=dataclasses_json.config(
        encoder=lambda d: add_prefix(d, prefix),
        decoder=lambda d: x.from_dict(remove_prefix(d, prefix))
    ))


def date_field(**kwargs):
    return dataclasses.field(metadata=dataclasses_json.config(
        encoder=str,
        decoder=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date(),
        mm_field=marshmallow.fields.Date(),
        **kwargs
    ))


def iso_datetime_field(**kwargs):
    return dataclasses.field(metadata=dataclasses_json.config(
        encoder=datetime.datetime.isoformat,
        decoder=datetime.datetime.fromisoformat,
        mm_field=marshmallow.fields.DateTime(format='iso'),
        **kwargs
    ))


class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
@json_prefix(prefix='competition_', exclude=['country_name'])
class Competition:
    id: int
    name: str
    gender: typing.Optional[Gender] = None
    country_name: typing.Optional[str] = None


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
@json_prefix(prefix='season_')
class Season:
    id: int
    name: str


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class CompetitionSeason:
    competition_id: int
    competition_name: str
    competition_gender: Gender
    country_name: str
    season_id: int
    season_name: str
    match_updated: datetime.datetime = iso_datetime_field()
    match_available: datetime.datetime = iso_datetime_field()

    competition: typing.Optional[Competition] = None
    season: typing.Optional[Season] = None

    def __post_init__(self):
        # Use object.__setattr__ to set attributes with frozen=True
        # https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
        competition = self.competition or Competition(
            id=self.competition_id,
            name=self.competition_name,
            gender=self.competition_gender,
            country_name=self.country_name
        )
        object.__setattr__(self, 'competition', competition)

        season = self.season or Season(
            id=self.season_id,
            name=self.season_name
        )
        object.__setattr__(self, 'season', season)


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Country:
    id: int
    name: str


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
@json_prefix(prefix='team_')
class Team:
    id: int
    name: str
    gender: typing.Optional[Gender] = None
    country: typing.Optional[Country] = None


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class CompetitionStage:
    id: int
    name: str


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Manager:
    id: int
    name: str
    nickname: str
    birth_date: str = date_field(metadata=dataclasses_json.config(field_name='dob'))
    country: typing.Optional[Country] = None
    # TODO: parse managers from match json


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Referee:
    id: int
    name: typing.Optional[str] = None
    country: typing.Optional[Country] = None
    # NOTE: could fix the name == 'None' issue with __post_init__, BUT then we couldn't
    #       freeze the class


class MatchStatus(enum.Enum):
    AVAILABLE = 'available'
    PROCESSING = 'processing'
    COLLECTING = 'collecting'
    SCHEDULED = 'scheduled'


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class MatchMetadata:
    data_version: typing.Optional[str] = None
    xy_fidelity_version: typing.Optional[str] = None
    shot_fidelity_version: typing.Optional[str] = None


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
@json_prefix(prefix='match_', include=['id', 'status'])
class Match:
    id: int
    competition: Competition
    season: Season
    date: datetime.date = date_field(metadata=dataclasses_json.config(field_name='match_date'))
    kick_off: datetime.time = dataclasses.field(metadata=dataclasses_json.config(
        encoder=str,
        decoder=lambda x: datetime.datetime.strptime(x, '%H:%M:%S.%f').time(),
        mm_field=marshmallow.fields.Time()
    ))
    match_week: int
    status: MatchStatus
    competition_stage: CompetitionStage
    home_team: Team = with_prefix(Team, 'home_')
    away_team: Team = with_prefix(Team, 'away_')
    home_score: typing.Optional[int]
    away_score: typing.Optional[int]
    referee: Referee
    metadata: MatchMetadata
    last_updated: datetime.datetime = iso_datetime_field()


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
@json_prefix(prefix='player_', exclude=['birth_date', 'country'])
class Player:
    id: int
    name: str
    birth_date: date_field()
    gender: Gender
    height: float
    weight: float
    country: Country
    nickname: typing.Optional[str] = None


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class PlayerLineup:
    jersey_number: int


class Lineup(typing.NamedTuple):
    team: Team
    lineup: typing.List[typing.Tuple[Player, PlayerLineup]]

    # TODO: from_json? to_dict? to_json?
    @staticmethod
    def from_dict(d):
        return Lineup(
            team=Team.from_dict(d),
            lineup=tuple((Player.from_dict(x), PlayerLineup.from_dict(x)) for x in d['lineup'])
        )


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class EventType:
    id: int
    name: str


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class PlayPattern:
    id: int
    name: str


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Position:
    id: int
    name: str


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class TacticPlayer:
    # TODO: better name
    player: Player  # NB no prefix
    position: Position


# @dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Tactics:
    formation: str
    # TODO: work out how to define this as a field with encoder and decoder? Maybe do the same for Lineup?
    lineup: typing.List[typing.Tuple[TacticPlayer, PlayerLineup]]

    def __post_init__(self):
        n_players = sum(int(i) for i in self.formation)
        if n_players > 10:
            raise TypeError(f'Formations must have 10 outfield players of fewer! {self.formation} has {n_players}.')


# Event qualifiers

@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class StatsBombObject:
    id: int
    name: str


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class FiftyFifty:
    outcome: StatsBombObject
    counterpress: typing.Optional[bool] = None


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class BadBehaviour:
    card: StatsBombObject


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class BallReceipt:
    outcome: StatsBombObject


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class BallRecovery:
    offensive: bool
    recovery_failure: bool


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Block:
    deflection: bool
    offensive: bool
    save_block: bool
    counterpress: bool


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Carry:
    end_location: typing.List[float]


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Clearance:
    aerial_won: bool
    body_part: StatsBombObject


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Dribble:
    overrun: bool
    nutmeg: bool
    outcome: StatsBombObject
    no_touch: typing.Optional[bool] = None


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class DribbledPast:
    counterpress: bool


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Duel:
    counterpress: bool
    type: StatsBombObject
    outcome: StatsBombObject


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class FoulCommitted:
    counterpress: bool
    offensive: bool
    type: StatsBombObject
    advantage: bool
    penalty: bool
    card: StatsBombObject


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class FoulWon:
    defensive: bool
    advantage: bool
    penalty: bool


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Goalkeeper:
    position: StatsBombObject
    technique: StatsBombObject
    body_part: StatsBombObject
    type: StatsBombObject
    outcome: StatsBombObject


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class HalfEnd:
    early_video_end: bool
    match_suspended: bool


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class HalfStart:
    late_video_start: bool


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class InjuryStoppage:
    in_chain: bool


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Interception:
    outcome: StatsBombObject


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Miscontrol:
    aerial_won: bool


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Pass:
    recipient: Player  # NB no prefix
    length: float
    angle: float
    height: StatsBombObject
    end_location: typing.List[float]
    body_part: StatsBombObject
    type: StatsBombObject
    outcome: typing.Optional[StatsBombObject] = None
    technique: typing.Optional[StatsBombObject] = None
    assisted_shot_id: typing.Optional[uuid.UUID] = None
    backheel: typing.Optional[bool] = None
    deflected: typing.Optional[bool] = None
    miscommunication: typing.Optional[bool] = None
    cross: typing.Optional[bool] = None
    cut_back: typing.Optional[bool] = None
    switch: typing.Optional[bool] = None
    shot_assist: typing.Optional[bool] = None
    goal_assist: typing.Optional[bool] = None


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class PlayerOff:
    permanent: bool


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Pressure:
    counterpress: bool


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Shot:
    key_pass_id: uuid.UUID
    end_location: typing.List[float]
    aerial_won: bool
    follows_dribble: bool
    first_time: bool
    freeze_frame: ...
    open_goal: bool
    statsbomb_xg: float
    deflected: bool
    technique: StatsBombObject
    body_part: StatsBombObject
    type: StatsBombObject
    outcome: StatsBombObject


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Substitution:
    replacement: Player
    outcome: StatsBombObject


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Event:
    id: uuid.UUID
    index: int
    period: int
    timestamp: ...
    minute: int
    second: int
    duration: float
    type: EventType
    possession: int
    possession_team: Team  # NB without prefix!
    play_pattern: PlayPattern
    team: Team  # NB without prefix!
    player: Player  # NB without prefix!
    position: Position
    location: typing.List[float]
    under_pressure: typing.Optional[bool]
    off_camera: typing.Optional[bool]
    out: typing.Optional[bool]
    related_events: typing.List[uuid.UUID]
    tactics: typing.Optional[uuid.UUID]

    # Nested event metadata
    fifty_fifty: typing.Optional[FiftyFifty] = dataclasses.field(metadata=dataclasses_json.config(field_name='50_50'))
    bad_behaviour: typing.Optional[BadBehaviour] = None
    ball_receipt: typing.Optional[BallReceipt] = None
    ball_recovery: typing.Optional[BallRecovery] = None
    block: typing.Optional[Block] = None
    carry: typing.Optional[Carry] = None
    clearance: typing.Optional[Clearance] = None
    dribble: typing.Optional[Dribble] = None
    dribbled_past: typing.Optional[DribbledPast] = None
    duel: typing.Optional[Duel] = None
    foul_committed: typing.Optional[FoulCommitted] = None
    foul_won: typing.Optional[FoulWon] = None
    goalkeeper: typing.Optional[Goalkeeper] = None
    half_end: typing.Optional[HalfEnd] = None
    half_start: typing.Optional[HalfStart] = None
    injury_stoppage: typing.Optional[InjuryStoppage] = None
    interception: typing.Optional[Interception] = None
    miscontrol: typing.Optional[Miscontrol] = None
    pass_: typing.Optional[Pass] = None
    player_off: typing.Optional[PlayerOff] = None
    pressure: typing.Optional[Pressure] = None
    shot: typing.Optional[Shot] = None
    substitution: typing.Optional[Substitution] = None


# Parse routes

def parse_competitions(response: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[CompetitionSeason]:
    return CompetitionSeason.schema().load(response, many=True)


def parse_matches(response: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[Match]:
    return [Match.from_dict(d) for d in response]


def parse_lineups(response: typing.List[typing.Dict[str, typing.Any]]) -> typing.Tuple[Lineup, Lineup]:
    l1, l2 = response
    return Lineup.from_dict(l1), Lineup.from_dict(l2)


def extract(target, obj):
    if isinstance(obj, target):
        yield obj
    elif isinstance(obj, collections.abc.Iterable):
        yield from _extract_iter(target, obj)
    elif dataclasses.is_dataclass(obj):
        yield from _extract_dataclass(target, obj)


def _extract_iter(target, obj):
    for o in obj:
        # Prevent infinite recursion in strings
        if o == obj:
            continue
        yield from extract(target, o)


def _extract_dataclass(target, obj):
    for field in dataclasses.fields(obj):
        field_value = getattr(obj, field.name)
        if isinstance(field_value, target):
            yield from extract(target, field_value)
