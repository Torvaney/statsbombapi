from . import ReadOnlyAdapter
from .utils import HTTPFetcher


class StatsbombServicesAdapter(ReadOnlyAdapter):
    def __init__(self, username, password):
        self._http_fetcher = HTTPFetcher(
            base_url='https://data.statsbombservices.com/api',
            auth=(username, password)
        )

    def get_competitions(self, version='v2'):
        return self._http_fetcher.get(f'/{version}/competitions')

    def get_matches(self, competition_id: int, season_id: int, version='v3'):
        return self._http_fetcher.get(f'/{version}/competitions/{competition_id}/seasons/{season_id}/matches')

    def get_lineups(self, match_id: int, version='v2'):
        return self._http_fetcher.get(f'/{version}/lineups/{match_id}')

    def get_events(self, match_id: int, version='v5'):
        return self._http_fetcher.get(f'/{version}/events/{match_id}')
