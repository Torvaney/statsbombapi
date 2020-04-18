import typing
from abc import ABC


from ...models import data


class Serializer(ABC):
    def unserialize_competitions(self, json) -> typing.List[data.CompetitionSeason]:
        raise NotImplementedError

    def unserialize_matches(self, json) -> typing.List[data.Match]:
        raise NotImplementedError

    def unserialize_linesup(self, json) -> typing.List[data.Lineup]:
        raise NotImplementedError

    def unserialize_events(self, json) -> typing.List[data.Event]:
        raise NotImplementedError
