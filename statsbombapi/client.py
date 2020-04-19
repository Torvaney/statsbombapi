import typing

from .models import data
from .infrastructure import (
    ReadOnlyRepositoryInterface, CachingRepositoryProxy,
    get_github_repository,
    get_local_repository,
    get_statsbomb_services_repository
)


class APIClient:
    def __init__(self, repository: ReadOnlyRepositoryInterface, caching_dir=None):
        self._repository = (
            repository
            if not caching_dir else
            CachingRepositoryProxy(repository=repository, base_dir=caching_dir)
        )

    def competitions(self) -> typing.List[data.CompetitionSeason]:
        """ Get competitions data from StatsBomb """
        return self._repository.get_competitions()

    def matches(self, competition_id: int, season_id: int) -> typing.List[data.Match]:
        """ Get matches data from StatsBomb """
        return self._repository.get_matches(competition_id, season_id)

    def lineups(self, match_id: int) -> typing.List[data.Lineup]:
        """ Get lineups data from StatsBomb """
        return self._repository.get_lineups(match_id)

    def events(self, match_id: int) -> typing.List[data.Event]:
        """ Get events data from StatsBomb """
        return self._repository.get_events(match_id)


def get_local_client(base_dir, **kwargs) -> APIClient:
    return APIClient(
        repository=get_local_repository(base_dir),
        **kwargs
    )


def get_public_client(**kwargs) -> APIClient:
    return APIClient(
        repository=get_github_repository(),
        **kwargs
    )


def get_api_client(username, password, **kwargs) -> APIClient:
    return APIClient(
        repository=get_statsbomb_services_repository(username, password),
        **kwargs
    )
