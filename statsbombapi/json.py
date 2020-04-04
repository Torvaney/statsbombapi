import enum
import typing

import dataclasses
import dataclasses_json


class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


def json_prefix(prefix, exclude=None):
    """ Add a json prefix to any dataclass attributes that do not have field information set. """
    def process(cls):
        for a_name in cls.__dict__.get('__annotations__', {}):
            if a_name in (exclude or []):
                continue
            if getattr(cls, a_name, None):
                continue

            field = dataclasses.field(metadata=dataclasses_json.config(field_name=prefix + a_name))
            setattr(cls, a_name, field)
        return cls
    return process


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
@json_prefix(prefix='competition_', exclude=['country_name'])
class Competition:
    id: int
    name: str
    country_name: typing.Optional[str]
    gender: typing.Optional[Gender]


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
@json_prefix(prefix='season_')
class Season:
    id: int
    name: str


@dataclasses_json.dataclass_json
@dataclasses.dataclass(frozen=True)
@json_prefix(prefix='match_')
class Match:
    id: int
    competition: Competition
