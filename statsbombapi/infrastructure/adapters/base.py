from abc import ABC, abstractmethod


class ReadOnlyAdapter(ABC):
    """ This is more like an interface than an abstract base class.. """

    @abstractmethod
    def get_competitions(self):
        raise NotImplementedError

    @abstractmethod
    def get_matches(self, competition_id: int, season_id: int):
        raise NotImplementedError

    @abstractmethod
    def get_lineups(self, match_id: int):
        raise NotImplementedError

    @abstractmethod
    def get_events(self, match_id: int):
        raise NotImplementedError