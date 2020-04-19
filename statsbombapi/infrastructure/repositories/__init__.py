import typing
from abc import ABC, abstractmethod

from ...exception import NotFound
from ..adapters import (
    ReadOnlyAdapter,
    ReadWriteAdapter,

    GithubHTTPSAdapter,
    LocalAdapter,
    StatsbombServicesAdapter
)
from ..serializers import (
    Serializer,
    DataclassesJsonSerializer,
    BinaryPickleSerializer
)

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


class RepositoryInterface(ReadOnlyRepositoryInterface):
    @abstractmethod
    def save_competitions(self, competitions: typing.List[data.CompetitionSeason]):
        raise NotImplementedError

    @abstractmethod
    def save_matches(self, competition_id: int, season_id: int, matches: typing.List[data.Match]):
        raise NotImplementedError

    @abstractmethod
    def save_lineups(self, match_id: int, lineups: typing.List[data.Lineup]):
        raise NotImplementedError

    @abstractmethod
    def save_events(self, match_id: int, events: typing.List[data.Event]):
        raise NotImplementedError


class _ReadMethodsMixin(object):
    _serializer: Serializer
    _adapter: ReadOnlyAdapter

    def get_competitions(self) -> typing.List[data.CompetitionSeason]:
        """ Get competitions data from StatsBomb """
        return self._serializer.unserialize_competitions(
            self._adapter.read_competitions()
        )

    def get_matches(self, competition_id: int, season_id: int) -> typing.List[data.Match]:
        """ Get matches data from StatsBomb """
        return self._serializer.unserialize_matches(
            self._adapter.read_matches(competition_id, season_id)
        )

    def get_lineups(self, match_id: int) -> typing.List[data.Lineup]:
        """ Get lineups data from StatsBomb """
        return self._serializer.unserialize_lineups(
            self._adapter.read_lineups(match_id)
        )

    def get_events(self, match_id: int) -> typing.List[data.Event]:
        """ Get events data from StatsBomb """
        return self._serializer.unserialize_events(
            self._adapter.read_events(match_id)
        )


class _WriteMethodsMixin(object):
    _serializer: Serializer
    _adapter: ReadWriteAdapter

    def save_competitions(self, competitions: typing.List[data.CompetitionSeason]):
        return self._adapter.write_competitions(
            self._serializer.serialize_competitions(competitions)
        )

    def save_matches(self, competition_id: int, season_id: int, matches: typing.List[data.Match]):
        return self._adapter.write_matches(
            competition_id, season_id,
            self._serializer.serialize_matches(matches)
        )

    def save_lineups(self, match_id: int, lineups: typing.List[data.Lineup]):
        return self._adapter.write_lineups(
            match_id,
            self._serializer.serialize_lineups(lineups)
        )

    def save_events(self, match_id: int, events: typing.List[data.Event]):
        return self._adapter.write_events(
            match_id,
            self._serializer.serialize_events(events)
        )


class ReadOnlyRepository(_ReadMethodsMixin, ReadOnlyRepositoryInterface):
    def __init__(self, adapter: ReadOnlyAdapter, serializer: Serializer):
        self._adapter = adapter
        self._serializer = serializer


class Repository(_ReadMethodsMixin, _WriteMethodsMixin, RepositoryInterface):
    def __init__(self, adapter: ReadWriteAdapter, serializer: Serializer):
        self._adapter = adapter
        self._serializer = serializer


class CachingRepositoryProxy(ReadOnlyRepositoryInterface):
    def __init__(self, repository: ReadOnlyRepositoryInterface, base_dir):
        self._origin_repository = repository
        self._cache_repository = Repository(
            adapter=LocalAdapter(base_dir, file_extension='pickle'),
            serializer=BinaryPickleSerializer()
        )

    def _check_cache(self, method_name, *args):

        cache_read = getattr(self._cache_repository, f"get_{method_name}")
        cache_write = getattr(self._cache_repository, f"save_{method_name}")
        origin_read = getattr(self._origin_repository, f"get_{method_name}")
        try:
            result = cache_read(*args)
        except NotFound:
            result = origin_read(*args)
            cache_write(*args, result)
        return result

    def get_competitions(self) -> typing.List[data.CompetitionSeason]:
        return self._check_cache("competitions")

    def get_matches(self, competition_id: int, season_id: int) -> typing.List[data.Match]:
        return self._check_cache("matches", competition_id, season_id)

    def get_lineups(self, match_id: int) -> typing.List[data.Lineup]:
        return self._check_cache("lineups", match_id)

    def get_events(self, match_id: int) -> typing.List[data.Event]:
        return self._check_cache("events", match_id)


def get_github_repository() -> ReadOnlyRepository:
    return ReadOnlyRepository(
        adapter=GithubHTTPSAdapter(),
        serializer=DataclassesJsonSerializer()
    )


def get_local_repository(base_dir) -> ReadOnlyRepository:
    return ReadOnlyRepository(
        adapter=LocalAdapter(base_dir, file_extension='json'),
        serializer=DataclassesJsonSerializer()
    )


def get_statsbomb_services_repository(username, password) -> ReadOnlyRepository:
    return ReadOnlyRepository(
        adapter=StatsbombServicesAdapter(username, password),
        serializer=DataclassesJsonSerializer()
    )
