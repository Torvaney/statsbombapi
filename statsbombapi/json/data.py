import dataclasses
import datetime
import enum
import marshmallow
import typing
import uuid

import dataclasses_json


def add_prefix(d: typing.Dict[str, typing.Any], prefix: str) -> typing.Dict[str, typing.Any]:
    """ Add a prefix to the keys of a dict. """
    return {prefix + k: v for k, v in d.items()}


def _strip_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def remove_prefix(d: typing.Dict[str, typing.Any], prefix: str) -> typing.Dict[str, typing.Any]:
    """ Remove a prefix from the keys of a dict. """
    return {_strip_prefix(k, prefix): v for k, v in d.items()}


def with_prefix(x, prefix):
    """ Add a prefix to a dataclass_json's encoder/decoder """
    return dataclasses.field(metadata=dataclasses_json.config(
        encoder=lambda d: add_prefix(d, prefix),
        decoder=lambda d: x.from_dict(remove_prefix(d, prefix))
    ))


def date_field(default=dataclasses.MISSING, **kwargs):
    return dataclasses.field(
        default=default,
        metadata=dataclasses_json.config(
            encoder=str,
            decoder=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date() if x else None,
            mm_field=marshmallow.fields.Date(),
            **kwargs
        )
    )


def iso_datetime_field(default=dataclasses.MISSING, **kwargs):
    return dataclasses.field(
        default=default,
        metadata=dataclasses_json.config(
            encoder=datetime.datetime.isoformat,
            decoder=lambda x: datetime.datetime.fromisoformat(str(x)) if x else None,
            mm_field=marshmallow.fields.DateTime(format='iso'),
            **kwargs
        )
    )


def time_field(default=dataclasses.MISSING, **kwargs):
    return dataclasses.field(
        default=default,
        metadata=dataclasses_json.config(
            encoder=str,
            decoder=lambda x: datetime.datetime.strptime(x, '%H:%M:%S.%f').time(),
            mm_field=marshmallow.fields.Time(),
            **kwargs
        )
    )


class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Competition:
    id: int
    name: str
    gender: typing.Optional[Gender] = None
    country_name: typing.Optional[str] = None


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
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
    match_updated: typing.Optional[datetime.datetime] = iso_datetime_field(default=None)
    match_available: typing.Optional[datetime.datetime] = iso_datetime_field(default=None)

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
    birth_date: str = date_field(field_name='dob')
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
    DELETED = 'deleted'


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class MatchMetadata:
    data_version: typing.Optional[str] = None
    xy_fidelity_version: typing.Optional[str] = None
    shot_fidelity_version: typing.Optional[str] = None


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Match:
    id: int = dataclasses.field(metadata=dataclasses_json.config(field_name='match_id'))
    competition: Competition = with_prefix(Competition, 'competition_')
    season: Season = with_prefix(Season, 'season_')
    date: datetime.date = date_field(field_name='match_date')
    kick_off: datetime.time = time_field()
    match_week: int
    metadata: MatchMetadata
    home_team: Team = with_prefix(Team, 'home_team_')
    away_team: Team = with_prefix(Team, 'away_team_')
    status: MatchStatus = dataclasses.field(metadata=dataclasses_json.config(field_name='match_status'))
    last_updated: datetime.datetime = iso_datetime_field()
    home_score: typing.Optional[int] = None
    away_score: typing.Optional[int] = None
    referee: typing.Optional[Referee] = None
    competition_stage: typing.Optional[CompetitionStage] = None


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Player:
    id: int
    name: str
    birth_date: typing.Optional[datetime.date] = date_field(
        field_name='birth_date',
        default=None
    )
    gender: typing.Optional[Gender] = None
    height: typing.Optional[float] = None
    weight: typing.Optional[float] = None
    country: typing.Optional[Country] = None
    nickname: typing.Optional[str] = None


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class LineupPlayer:
    player_id: int
    player_name: str
    country: Country
    jersey_number: int
    birth_date: typing.Optional[datetime.date] = date_field(default=None, field_name='birth_date')
    player_height: typing.Optional[float] = None
    player_weight: typing.Optional[float] = None
    player_gender: typing.Optional[Gender] = None
    player_nickname: typing.Optional[str] = None

    player: typing.Optional[Player] = None

    def __post_init__(self):
        player = self.player or Player(
            id=self.player_id,
            name=self.player_name,
            nickname=self.player_nickname,
            birth_date=self.birth_date,
            gender=self.player_gender,
            weight=self.player_weight,
            height=self.player_height,
            country=self.country
        )
        object.__setattr__(self, 'player', player)


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Lineup:
    team_id: int
    team_name: int
    lineup: typing.List[LineupPlayer]

    team: typing.Optional[Team] = None

    def __post_init__(self):
        team = self.team or Team(
            id=self.team_id,
            name=self.team_name
        )
        object.__setattr__(self, 'team', team)


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
    jersey_number: int


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Tactics:
    formation: int
    lineup: typing.List[TacticPlayer]

    def __post_init__(self):
        object.__setattr__(self, 'formation', str(self.formation))


# Event qualifiers

class EventMetadata:
    pass


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class StatsBombObject:
    id: int
    name: str


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class FiftyFifty(EventMetadata):
    outcome: StatsBombObject
    counterpress: typing.Optional[bool] = None


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class BadBehaviour(EventMetadata):
    card: StatsBombObject


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class BallReceipt(EventMetadata):
    outcome: StatsBombObject


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class BallRecovery(EventMetadata):
    recovery_failure: typing.Optional[bool] = None
    offensive: typing.Optional[bool] = None


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class Block(EventMetadata):
    deflection: typing.Optional[bool] = None
    offensive: typing.Optional[bool] = None
    save_block: typing.Optional[bool] = None
    counterpress: typing.Optional[bool] = None


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class Carry(EventMetadata):
    end_location: typing.List[float]


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class Clearance(EventMetadata):
    body_part: typing.Optional[StatsBombObject] = None
    aerial_won: typing.Optional[bool] = None


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class Dribble(EventMetadata):
    outcome: StatsBombObject
    overrun: typing.Optional[bool] = None
    nutmeg: typing.Optional[bool] = None
    no_touch: typing.Optional[bool] = None


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class DribbledPast(EventMetadata):
    counterpress: bool


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class Duel(EventMetadata):
    type: typing.Optional[StatsBombObject] = None
    outcome: typing.Optional[StatsBombObject] = None
    counterpress: typing.Optional[bool] = None


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class FoulCommitted(EventMetadata):
    type: typing.Optional[StatsBombObject] = None
    card: typing.Optional[StatsBombObject] = None
    penalty: typing.Optional[bool] = None
    advantage: typing.Optional[bool] = None
    offensive: typing.Optional[bool] = None
    counterpress: typing.Optional[bool] = None


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class FoulWon(EventMetadata):
    defensive: typing.Optional[bool] = None
    advantage: typing.Optional[bool] = None
    penalty: typing.Optional[bool] = None


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class Goalkeeper(EventMetadata):
    outcome: typing.Optional[StatsBombObject] = None
    body_part: typing.Optional[StatsBombObject] = None
    position: typing.Optional[StatsBombObject] = None
    technique: typing.Optional[StatsBombObject] = None
    type: typing.Optional[StatsBombObject] = None
    end_location: typing.Optional[typing.List[float]] = None


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class HalfEnd(EventMetadata):
    early_video_end: bool
    match_suspended: bool


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class HalfStart(EventMetadata):
    late_video_start: bool


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class InjuryStoppage(EventMetadata):
    in_chain: bool


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class Interception(EventMetadata):
    outcome: StatsBombObject


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class Miscontrol(EventMetadata):
    aerial_won: typing.Optional[bool] = None


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class Pass(EventMetadata):
    length: float
    angle: float
    height: StatsBombObject
    end_location: typing.List[float]
    recipient: typing.Optional[Player] = None
    body_part: typing.Optional[StatsBombObject] = None
    type: typing.Optional[StatsBombObject] = None
    outcome: typing.Optional[StatsBombObject] = None
    technique: typing.Optional[StatsBombObject] = None
    aerial_won: typing.Optional[bool] = None
    assisted_shot_id: typing.Optional[uuid.UUID] = None
    backheel: typing.Optional[bool] = None
    deflected: typing.Optional[bool] = None
    miscommunication: typing.Optional[bool] = None
    cross: typing.Optional[bool] = None
    cut_back: typing.Optional[bool] = None
    switch: typing.Optional[bool] = None
    shot_assist: typing.Optional[bool] = None
    goal_assist: typing.Optional[bool] = None
    xclaim: typing.Optional[float] = None


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class PlayerOff(EventMetadata):
    permanent: bool


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Pressure(EventMetadata):
    counterpress: bool


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class FreezeFrame(EventMetadata):
    location: typing.List[float]
    player: Player
    position: Position
    teammate: bool


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.EXCLUDE)
@dataclasses.dataclass(frozen=True)
class Shot(EventMetadata):
    end_location: typing.List[float]
    statsbomb_xg: float
    technique: StatsBombObject
    body_part: StatsBombObject
    type: StatsBombObject
    outcome: StatsBombObject
    freeze_frame: typing.Optional[typing.List[FreezeFrame]] = None
    key_pass_id: typing.Optional[uuid.UUID] = None
    aerial_won: typing.Optional[bool] = None
    follows_dribble: typing.Optional[bool] = None
    first_time: typing.Optional[bool] = None
    open_goal: typing.Optional[bool] = None
    deflected: typing.Optional[bool] = None
    one_on_one: typing.Optional[bool] = None
    statsbomb_xg2: typing.Optional[float] = None


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Substitution(EventMetadata):
    replacement: Player
    outcome: StatsBombObject


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
class Event:
    id: uuid.UUID
    index: int
    period: int
    timestamp: datetime.time = time_field()
    minute: int
    second: int
    type: EventType
    possession: int
    possession_team: Team
    play_pattern: PlayPattern
    team: Team
    duration: typing.Optional[float] = None
    related_events: typing.List[uuid.UUID] = dataclasses.field(default_factory=lambda: [])
    location: typing.Optional[typing.List[float]] = None
    under_pressure: typing.Optional[bool] = None
    off_camera: typing.Optional[bool] = None
    out: typing.Optional[bool] = None
    player: typing.Optional[Player] = None
    position: typing.Optional[Position] = None
    tactics: typing.Optional[Tactics] = None
    counterpress: typing.Optional[bool] = None

    # Nested event metadata
    fifty_fifty: typing.Optional[FiftyFifty] = dataclasses.field(
        default=None,
        metadata=dataclasses_json.config(field_name='50_50')
    )
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
    pass_: typing.Optional[Pass] = dataclasses.field(
        default=None,
        metadata=dataclasses_json.config(field_name='pass')
    )
    player_off: typing.Optional[PlayerOff] = None
    pressure: typing.Optional[Pressure] = None
    shot: typing.Optional[Shot] = None
    substitution: typing.Optional[Substitution] = None
