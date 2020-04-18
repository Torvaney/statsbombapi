import collections.abc
import dataclasses
import typing

from . import data


# Parse routes

def parse_competitions(json: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[data.CompetitionSeason]:
    return data.CompetitionSeason.schema().load(json, many=True)


def parse_matches(json: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[data.Match]:
    return [data.Match.from_dict(d) for d in json]


def parse_lineups(json: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[data.Lineup]:
    l1, l2 = json
    return [data.Lineup.from_dict(l1), data.Lineup.from_dict(l2)]


def parse_events(json: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[data.Event]:
    return data.Event.schema().load(json, many=True)


# Extracting objects from parsed json

def extract(target, obj):
    """
    Recursively extract any objects within `obj` that are instances of `target`.

    If `obj` is a dataclass, extract will search each field's values for instances
    of `target`.
    """
    if isinstance(obj, target):
        yield obj
    elif isinstance(obj, collections.abc.Iterable):
        yield from _extract_from_iter(target, obj)
    elif dataclasses.is_dataclass(obj):
        yield from _extract_from_dataclass(target, obj)


def _extract_from_iter(target, obj):
    for o in obj:
        # Prevent infinite recursion in strings
        if o == obj:
            continue
        yield from extract(target, o)


def _extract_from_dataclass(target, obj):
    for field in dataclasses.fields(obj):
        field_value = getattr(obj, field.name)
        yield from extract(target, field_value)
