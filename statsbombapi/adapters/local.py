import warnings

from . import ReadOnlyAdapter
from .utils import LocalFileSystem


class LocalAdapter(ReadOnlyAdapter):
    def __init__(self, base_path):
        statsbomb_data_advice = (
            'Please be responsible with Statsbomb data and make sure you have '
            'registered your details on https://www.statsbomb.com/resource-centre, '
            'and read and accepted the User Agreement (available on the same page).'
        )
        warnings.warn(statsbomb_data_advice)
        self._local_reader = LocalFileSystem(base_path)

    def get_competitions(self):
        return self._local_reader.read('/competitions.json')

    def get_matches(self, competition_id: int, season_id: int):
        return self._local_reader.read(f'/matches/{competition_id}/{season_id}.json')

    def get_lineups(self, match_id: int):
        return self._local_reader.read(f'/lineups/{match_id}.json')

    def get_events(self, match_id: int):
        return self._local_reader.read(f'/events/{match_id}.json')

