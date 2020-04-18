import typing

from .adapters import ReadOnlyAdapter, GithubAdapter, StatsbombServicesAdapter, LocalAdapter
from .models import data, parse


class APIClient:
    def __init__(self, adapter: ReadOnlyAdapter):
        self._adapter = adapter

    def competitions(self) -> typing.List[data.CompetitionSeason]:
        """ Get competitions data from StatsBomb """
        return parse.parse_competitions(
            json=self._adapter.get_competitions()
        )

    def matches(self, competition_id: int, season_id: int) -> typing.List[data.Match]:
        """ Get matches data from StatsBomb """
        return parse.parse_matches(
            json=self._adapter.get_matches(competition_id, season_id)
        )

    def lineups(self, match_id: int) -> typing.List[data.Lineup]:
        """ Get lineups data from StatsBomb """
        return parse.parse_lineups(
            json=self._adapter.get_lineups(match_id)
        )

    def events(self, match_id: int) -> typing.List[data.Event]:
        """ Get events data from StatsBomb """
        return parse.parse_events(
            json=self._adapter.get_events(match_id)
        )


def get_local_client(base_path) -> APIClient:
    return APIClient(
        adapter=LocalAdapter(base_path)
    )


def get_public_client() -> APIClient:
    return APIClient(
        adapter=GithubAdapter()
    )


def get_api_client(username, password) -> APIClient:
    return APIClient(
        adapter=StatsbombServicesAdapter(username, password)
    )
