import os

import requests
import json

from ..exception import StatsbombAPIException


class HTTPFetcher(object):
    def __init__(self, base_url, auth=None):
        self._base_url = base_url
        self._auth = auth

    @staticmethod
    def handle_non_ok_code(response):
        raise StatsbombAPIException(
            f'Unexpected error code when trying to reach {response.url}: {response.status_code}')

    def get(self, path):
        response = requests.get(
            f"{self._base_url}/{path}",
            auth=self._auth
        )
        if response.status_code != 200:
            self.handle_non_ok_code(response)
        return response.json()


class LocalFileSystem(object):
    def __init__(self, base_path):
        self._base_path = base_path

    def read(self, path):
        file_path = f"{self._base_path}/{path}"
        if not os.path.exists(file_path):
            raise StatsbombAPIException(
                f'Local file "{path}" does not exist. Please make sure the '
                f'base_path is correct and you local files are up-to-date'
            )

        with open(file_path, "r", encoding='utf8') as fp:
            return json.load(fp)



