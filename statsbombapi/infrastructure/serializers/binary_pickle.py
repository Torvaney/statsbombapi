import typing
from pickle import loads, dumps

from . import Serializer


from ...models import data


class BinaryPickleSerializer(Serializer):
    def unserialize_competitions(self, s: bytes) -> typing.List[data.CompetitionSeason]:
        return loads(s)

    def unserialize_matches(self, s: bytes) -> typing.List[data.Match]:
        return loads(s)

    def unserialize_lineups(self, s: bytes) -> typing.List[data.Lineup]:
        return loads(s)

    def unserialize_events(self, s: bytes) -> typing.List[data.Event]:
        return loads(s)

    def serialize_competitions(self, competitions: typing.List[data.CompetitionSeason]) -> bytes:
        return dumps(competitions)

    def serialize_matches(self, matches: typing.List[data.Match]) -> bytes:
        return dumps(matches)

    def serialize_lineups(self, lineups: typing.List[data.Lineup]) -> bytes:
        return dumps(lineups)

    def serialize_events(self, events: typing.List[data.Event]) -> bytes:
        return dumps(events)
