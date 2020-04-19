from abc import ABC, abstractmethod


class ReadOnlyAdapter(ABC):
    """ This is more like an interface than an abstract base class.. """

    @abstractmethod
    def read_competitions(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def read_matches(self, competition_id: int, season_id: int) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def read_lineups(self, match_id: int) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def read_events(self, match_id: int) -> bytes:
        raise NotImplementedError


class ReadWriteAdapter(ReadOnlyAdapter):
    @abstractmethod
    def write_competitions(self, s: bytes):
        raise NotImplementedError

    @abstractmethod
    def write_matches(self, competition_id: int, season_id: int, s: bytes):
        raise NotImplementedError

    @abstractmethod
    def write_lineups(self, match_id: int, s: bytes):
        raise NotImplementedError

    @abstractmethod
    def write_events(self, match_id: int, s: bytes):
        raise NotImplementedError
