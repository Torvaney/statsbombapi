import warnings

from . import ReadOnlyAdapter
from .utils import HTTPFetcher


class GithubAdapter(ReadOnlyAdapter):
    def __init__(self):
        statsbomb_data_advice = (
            'Please be responsible with Statsbomb data and make sure you have '
            'registered your details on https://www.statsbomb.com/resource-centre, '
            'and read and accepted the User Agreement (available on the same page).'
        )
        warnings.warn(statsbomb_data_advice)

        self._http_fetcher = HTTPFetcher(
            base_url='https://raw.githubusercontent.com/statsbomb/open-data/master/data'
        )

    def get_competitions(self):
        return self._http_fetcher.get('/competitions.json')

    def get_matches(self, competition_id: int, season_id: int):
        return self._http_fetcher.get(f'/matches/{competition_id}/{season_id}.json')

    def get_lineups(self, match_id: int):
        return self._http_fetcher.get(f'/lineups/{match_id}.json')

    def get_events(self, match_id: int):
        return self._http_fetcher.get(f'/events/{match_id}.json')

