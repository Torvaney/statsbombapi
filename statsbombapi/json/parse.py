import collections.abc
import dataclasses
import typing

from statsbombapi.json import data


# Parse routes

def parse_competitions(response: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[data.CompetitionSeason]:
    return data.CompetitionSeason.schema().load(response, many=True)


def parse_matches(response: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[data.Match]:
    return [data.Match.from_dict(d) for d in response]


def parse_lineups(response: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[data.Lineup]:
    l1, l2 = response
    return [data.Lineup.from_dict(l1), data.Lineup.from_dict(l2)]


def parse_events(response: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[data.Event]:
    return data.Event.schema().load(response, many=True)


# Extracting objects from parsed json

def extract(target, obj):
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
