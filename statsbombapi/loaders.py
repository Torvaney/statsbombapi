import requests
import warnings


class StatsbombAPIException(Exception):
    pass


class HTTPFetcher:
    def __init__(self, base_url, auth=None):
        self._base_url = base_url
        self._auth = auth

    @staticmethod
    def handle_non_ok_code(response):
        try:
            response.raise_for_status()
        except requests.exceptions.BaseHTTPError as err:
            raise StatsbombAPIException(
                f'Unexpected error code when trying to reach {response.url}: {response.status_code}'
            ) from err

    def get(self, path) -> bytes:
        response = requests.get(
            f'{self._base_url}/{path}',
            auth=self._auth
        )
        if response.status_code != 200:
            self.handle_non_ok_code(response)
        return response.content


class StatsbombAPILoader:
    def __init__(self, username, password):
        self._http_fetcher = HTTPFetcher(
            base_url='https://data.statsbombservices.com/api',
            auth=(username, password)
        )

    def load_competitions(self, version='v2'):
        return self._http_fetcher.get(f'{version}/competitions')

    def load_matches(self, competition_id, season_id, version='v3'):
        return self._http_fetcher.get(f'{version}/competitions/{competition_id}/seasons/{season_id}/matches')

    def load_lineups(self, match_id, version='v2'):
        return self._http_fetcher.get(f'{version}/lineups/{match_id}')

    def load_events(self, match_id, version='v5'):
        return self._http_fetcher.get(f'{version}/events/{match_id}')


class OpenDataLoader:
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

    def load_competitions(self):
        return self._http_fetcher.get('competitions.json')

    def load_matches(self, competition_id: int, season_id: int):
        return self._http_fetcher.get(f'matches/{competition_id}/{season_id}.json')

    def load_lineups(self, match_id: int):
        return self._http_fetcher.get(f'lineups/{match_id}.json')

    def load_events(self, match_id: int):
        return self._http_fetcher.get(f'events/{match_id}.json')


class LocalLoader:
    def __init__(self, base_dir, file_extension):
        self._base_dir = base_dir
        self._file_extension = file_extension

    def _read(self, path) -> bytes:
        file_path = f'{self._base_dir}/{path}.{self._file_extension}'
        with open(file_path, "rb") as fp:
            return fp.read()

    def load_competitions(self):
        return self._read('competitions')

    def load_matches(self, competition_id, season_id):
        return self._read(f'matches/{competition_id}/{season_id}')

    def load_lineups(self, match_id):
        return self._read(f'lineups/{match_id}')

    def load_events(self, match_id):
        return self._read(f'events/{match_id}')
