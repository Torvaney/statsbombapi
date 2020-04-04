import datetime
import enum
import marshmallow
import typing

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
class DataUpdate:
    # TODO: come up with a better name for this!
    match_updated: datetime.datetime = iso_datetime_field()
    match_available: datetime.datetime = iso_datetime_field()


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

    @staticmethod
    def from_dict(d):
        return Lineup(
            team=Team.from_dict(d),
            lineup=tuple((Player.from_dict(x), PlayerLineup.from_dict(x)) for x in d['lineup'])
        )


def parse_competitions(response: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[typing.Tuple[Competition, Season, DataUpdate]]:
    competitions = Competition.schema().load(response, many=True, unknown='EXCLUDE')
    seasons = Season.schema().load(response, many=True, unknown='EXCLUDE')
    updates = DataUpdate.schema().load(response, many=True, unknown='EXCLUDE')
    return list(zip(competitions, seasons, updates))


def parse_matches(response: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[Match]:
    return [Match.from_dict(d) for d in response]


def parse_lineups(response: typing.List[typing.Dict[str, typing.Any]]) -> typing.Tuple[Lineup, Lineup]:
    l1, l2 = response
    return Lineup.from_dict(l1), Lineup.from_dict(l2)
