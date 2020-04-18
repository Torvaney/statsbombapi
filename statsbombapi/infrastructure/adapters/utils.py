import requests

from ...exception import StatsbombAPIException


class HTTPFetcher(object):
    def __init__(self, base_url, auth=None):
        self._base_url = base_url
        self._auth = auth

    @staticmethod
    def handle_non_ok_code(response):
        """
            Subclass this method to handle non-200 error codes in a specific way.
            For example, you may want to add logging
        """
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



