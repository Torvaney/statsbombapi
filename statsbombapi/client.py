import typing

import requests

import statsbombapi.json

from statsbombapi.json import data


class StatsbombAPIException(Exception):
    pass


class BaseAPIClient:
    def __init__(self):
        pass

    @staticmethod
    def _get_competitions():
        raise NotImplementedError

    @staticmethod
    def _get_matches(competition_id, season_id):
        raise NotImplementedError

    @staticmethod
    def _get_lineups(match_id):
        raise NotImplementedError

    @staticmethod
    def _get_events(match_id):
        raise NotImplementedError

    @staticmethod
    def _unwrap_response(response):
        if response.status_code != 200:
            self.handle_non_ok_code(response)
        return response.json()

    @staticmethod
    def handle_non_ok_code(response):
        """
        Subclass this method to handle non-200 error codes in a specific way.
        For example, you may want to add logging
        """
        raise StatsbombAPIException(f'Unexpected error code when trying to reach {response.url}: {response.status_code}')

    def _get_and_parse(self, response, parse):
        response_json = self._unwrap_response(response)
        parsed = parse(response_json)
        return parsed

    def competitions(self) -> typing.List[typing.Tuple[data.Competition, data.Season]]:
        """ Get competitions data from StatsBomb """
        return self._get_and_parse(
            self._get_competitions(),
            statsbombapi.json.parse_competitions
        )

    def matches(self, competition_id: int, season_id: int) -> typing.List[data.Match]:
        """ Get matches data from StatsBomb """
        return self._get_and_parse(
            self._get_matches(competition_id, season_id),
            statsbombapi.json.parse_matches
        )

    def lineups(self, match_id: int) -> typing.List[data.Lineup]:
        """ Get lineups data from StatsBomb """
        return self._get_and_parse(
            self._get_lineups(match_id),
            statsbombapi.json.parse_lineups
        )

    def events(self, match_id: int) -> typing.List[data.Event]:
        """ Get events data from StatsBomb """
        return self._get_and_parse(
            self._get_events(match_id),
            statsbombapi.json.parse_events
        )


class StatsbombPublic(BaseAPIClient):
    BASE_URL = 'https://raw.githubusercontent.com/statsbomb/open-data/master/data'

    def _get_competitions(self):
        return requests.get(f'{self.BASE_URL}/competitions.json')

    def _get_matches(self, competition_id, season_id):
        return requests.get(f'{self.BASE_URL}/matches/{competition_id}/{season_id}.json')

    def _get_lineups(self, match_id):
        return requests.get(f'{self.BASE_URL}/lineups/{match_id}.json')

    def _get_events(self, match_id):
        return requests.get(f'{self.BASE_URL}/events/{match_id}.json')


class StatsbombAPI(BaseAPIClient):
    BASE_URL = 'https://data.statsbombservices.com/api'

    def __init__(self, username, password):
        self.auth = (username, password)

    def _get_competitions(self, version='v2'):
        return requests.get(f'{self.BASE_URL}/{version}/competitions', auth=self.auth)

    def _get_matches(self, competition_id, season_id, version='v3'):
        return requests.get(f'{self.BASE_URL}/{version}/competitions/{competition_id}/seasons/{season_id}/matches', auth=self.auth)

    def _get_lineups(self, match_id, version='v2'):
        return requests.get(f'{self.BASE_URL}/{version}/lineups/{match_id}')

    def _get_events(self, match_id, version='v5'):
        return requests.get(f'{self.BASE_URL}/{version}/events/{match_id}')
