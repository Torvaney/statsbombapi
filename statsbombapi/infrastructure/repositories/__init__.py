import os
import pickle
import typing
from abc import ABC, abstractmethod

from ..adapters import GithubHTTPSAdapter, LocalAdapter, StatsbombServicesAdapter
from ..serializers import DataclassesJsonSerializer
from ..adapters import ReadOnlyAdapter
from ..serializers import Serializer

from ...models import data


class ReadOnlyRepositoryInterface(ABC):
    @abstractmethod
    def get_competitions(self) -> typing.List[data.CompetitionSeason]:
        raise NotImplementedError

    @abstractmethod
    def get_matches(self, competition_id: int, season_id: int) -> typing.List[data.Match]:
        raise NotImplementedError

    @abstractmethod
    def get_lineups(self, match_id: int) -> typing.List[data.Lineup]:
        raise NotImplementedError

    @abstractmethod
    def get_events(self, match_id: int) -> typing.List[data.Event]:
        raise NotImplementedError


class ReadOnlyRepository(ReadOnlyRepositoryInterface):
    def __init__(self, adapter: ReadOnlyAdapter, serializer: Serializer):
        self._adapter = adapter
        self._serializer = serializer

    def get_competitions(self) -> typing.List[data.CompetitionSeason]:
        """ Get competitions data from StatsBomb """
        return self._serializer.unserialize_competitions(
            json=self._adapter.get_competitions()
        )

    def get_matches(self, competition_id: int, season_id: int) -> typing.List[data.Match]:
        """ Get matches data from StatsBomb """
        return self._serializer.unserialize_matches(
            json=self._adapter.get_matches(competition_id, season_id)
        )

    def get_lineups(self, match_id: int) -> typing.List[data.Lineup]:
        """ Get lineups data from StatsBomb """
        return self._serializer.unserialize_linesup(
            json=self._adapter.get_lineups(match_id)
        )

    def get_events(self, match_id: int) -> typing.List[data.Event]:
        """ Get events data from StatsBomb """
        return self._serializer.unserialize_events(
            json=self._adapter.get_events(match_id)
        )


class CachingRepositoryProxy(ReadOnlyRepositoryInterface):
    def __init__(self, repository: ReadOnlyRepositoryInterface, base_dir):
        self._repository = repository
        self._base_dir = base_dir

    def _check_cache(self, cache_key, origin_fn):
        file_path = f"{self._base_dir}/{cache_key}.pickle"

        if not os.path.exists(file_path):
            result = origin_fn()

            with open(file_path, "wb") as fp:
                pickle.dump(result, fp)
        else:
            with open(file_path, "rb") as fp:
                result = pickle.load(fp)
        return result

    def get_competitions(self) -> typing.List[data.CompetitionSeason]:
        return self._check_cache(
            cache_key="competitions",
            origin_fn=lambda: self._repository.get_competitions()
        )

    def get_matches(self, competition_id: int, season_id: int) -> typing.List[data.Match]:
        return self._check_cache(
            cache_key=f"matches-{competition_id}-{season_id}",
            origin_fn=lambda: self._repository.get_matches(competition_id, season_id)
        )

    def get_lineups(self, match_id: int) -> typing.List[data.Lineup]:
        return self._check_cache(
            cache_key=f"lineups-{match_id}",
            origin_fn=lambda: self._repository.get_lineups(match_id)
        )

    def get_events(self, match_id: int) -> typing.List[data.Event]:
        return self._check_cache(
            cache_key=f"events-{match_id}",
            origin_fn=lambda: self._repository.get_events(match_id)
        )


def get_github_repository() -> ReadOnlyRepository:
    return ReadOnlyRepository(
        adapter=GithubHTTPSAdapter(),
        serializer=DataclassesJsonSerializer()
    )


def get_local_repository(base_dir) -> ReadOnlyRepository:
    return ReadOnlyRepository(
        adapter=LocalAdapter(base_dir),
        serializer=DataclassesJsonSerializer()
    )


def get_statsbomb_services_repository(username, password) -> ReadOnlyRepository:
    return ReadOnlyRepository(
        adapter=StatsbombServicesAdapter(username, password),
        serializer=DataclassesJsonSerializer()
    )
