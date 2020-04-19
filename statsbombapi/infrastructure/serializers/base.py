import typing
from abc import ABC, abstractmethod

from ...models import data


class Serializer(ABC):
    @abstractmethod
    def unserialize_competitions(self, s: bytes) -> typing.List[data.CompetitionSeason]:
        raise NotImplementedError

    @abstractmethod
    def unserialize_matches(self, s: bytes) -> typing.List[data.Match]:
        raise NotImplementedError

    @abstractmethod
    def unserialize_lineups(self, s: bytes) -> typing.List[data.Lineup]:
        raise NotImplementedError

    @abstractmethod
    def unserialize_events(self, s: bytes) -> typing.List[data.Event]:
        raise NotImplementedError

    @abstractmethod
    def serialize_competitions(self, competitions: typing.List[data.CompetitionSeason]) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def serialize_matches(self, matches: typing.List[data.Match]) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def serialize_lineups(self, lineups: typing.List[data.Lineup]) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def serialize_events(self, events: typing.List[data.Event]) -> bytes:
        raise NotImplementedError
