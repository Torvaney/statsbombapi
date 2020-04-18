import typing

from . import Serializer

from ...models import data, parse


class DataclassesJsonSerializer(Serializer):
    def unserialize_competitions(self, json) -> typing.List[data.CompetitionSeason]:
        return parse.parse_competitions(json)

    def unserialize_matches(self, json) -> typing.List[data.Match]:
        return parse.parse_matches(json)

    def unserialize_linesup(self, json) -> typing.List[data.Lineup]:
        return parse.parse_lineups(json)

    def unserialize_events(self, json) -> typing.List[data.Event]:
        return parse.parse_events(json)
