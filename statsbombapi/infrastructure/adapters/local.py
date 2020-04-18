import json
import os
import warnings

from ...exception import StatsbombAPIException
from . import ReadOnlyAdapter


class LocalAdapter(ReadOnlyAdapter):
    def __init__(self, base_dir):
        statsbomb_data_advice = (
            'Please be responsible with Statsbomb data and make sure you have '
            'registered your details on https://www.statsbomb.com/resource-centre, '
            'and read and accepted the User Agreement (available on the same page).'
        )
        warnings.warn(statsbomb_data_advice)
        self._base_dir = base_dir

    def _read(self, path):
        file_path = f"{self._base_dir}/{path}"
        if not os.path.exists(file_path):
            raise StatsbombAPIException(
                f'Local file "{path}" does not exist. Please make sure the '
                f'base_path is correct and you local files are up-to-date'
            )

        with open(file_path, "r", encoding='utf8') as fp:
            return json.load(fp)

    def get_competitions(self):
        return self._read('/competitions.json')

    def get_matches(self, competition_id: int, season_id: int):
        return self._read(f'/matches/{competition_id}/{season_id}.json')

    def get_lineups(self, match_id: int):
        return self._read(f'/lineups/{match_id}.json')

    def get_events(self, match_id: int):
        return self._read(f'/events/{match_id}.json')

