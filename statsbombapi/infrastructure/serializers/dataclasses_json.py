import typing
from json import loads

from . import Serializer

from ...models import data, parse


class DataclassesJsonSerializer(Serializer):
    def unserialize_competitions(self, s: bytes) -> typing.List[data.CompetitionSeason]:
        return parse.parse_competitions(
            loads(s)
        )

    def unserialize_matches(self, s: bytes) -> typing.List[data.Match]:
        return parse.parse_matches(
            loads(s)
        )

    def unserialize_lineups(self, s: bytes) -> typing.List[data.Lineup]:
        return parse.parse_lineups(
            loads(s)
        )

    def unserialize_events(self, s: bytes) -> typing.List[data.Event]:
        return parse.parse_events(
            loads(s)
        )

    def serialize_competitions(self, competitions: typing.List[data.CompetitionSeason]) -> bytes:
        raise NotImplementedError

    def serialize_matches(self, matches: typing.List[data.Match]) -> bytes:
        raise NotImplementedError

    def serialize_lineups(self, lineups: typing.List[data.Lineup]) -> bytes:
        raise NotImplementedError

    def serialize_events(self, events: typing.List[data.Event]) -> bytes:
        raise NotImplementedError
