import os
import warnings

from ...exception import NotFound
from . import ReadWriteAdapter


class LocalAdapter(ReadWriteAdapter):
    def __init__(self, base_dir, file_extension):
        statsbomb_data_advice = (
            'Please be responsible with Statsbomb data and make sure you have '
            'registered your details on https://www.statsbomb.com/resource-centre, '
            'and read and accepted the User Agreement (available on the same page).'
        )
        warnings.warn(statsbomb_data_advice)
        self._base_dir = base_dir
        self._file_extension = file_extension

    def _read(self, path) -> bytes:
        file_path = f"{self._base_dir}/{path}.{self._file_extension}"
        if not os.path.exists(file_path):
            raise NotFound(
                f'Local file "{path}" does not exist. Please make sure the '
                f'base_path is correct and you local files are up-to-date'
            )

        with open(file_path, "rb") as fp:
            return fp.read()

    def _write(self, path, s: bytes):
        file_path = f"{self._base_dir}/{path}.{self._file_extension}"
        dir_name = os.path.dirname(file_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        with open(file_path, "wb") as fp:
            fp.write(s)

    def read_competitions(self) -> bytes:
        return self._read('/competitions')

    def read_matches(self, competition_id: int, season_id: int) -> bytes:
        return self._read(f'/matches/{competition_id}/{season_id}')

    def read_lineups(self, match_id: int) -> bytes:
        return self._read(f'/lineups/{match_id}')

    def read_events(self, match_id: int) -> bytes:
        return self._read(f'/events/{match_id}')

    def write_competitions(self, s: bytes):
        return self._write('/competitions', s)

    def write_matches(self, competition_id: int, season_id: int, s: bytes):
        return self._write(f'/matches/{competition_id}/{season_id}', s)

    def write_lineups(self, match_id: int, s: bytes):
        return self._write(f'/lineups/{match_id}', s)

    def write_events(self, match_id: int, s: bytes):
        return self._write(f'/events/{match_id}', s)


