
class Repository(object):
    def __init__(self, adapter: ReadOnlyAdapter, serializer):

    def competitions(self) -> typing.List[data.CompetitionSeason]:
        """ Get competitions data from StatsBomb """
        return parse.parse_competitions(
            json=self._adapter.get_competitions()
        )

    def matches(self, competition_id: int, season_id: int) -> typing.List[data.Match]:
        """ Get matches data from StatsBomb """
        return parse.parse_matches(
            json=self._adapter.get_matches(competition_id, season_id)
        )

    def lineups(self, match_id: int) -> typing.List[data.Lineup]:
        """ Get lineups data from StatsBomb """
        return parse.parse_lineups(
            json=self._adapter.get_lineups(match_id)
        )

    def events(self, match_id: int) -> typing.List[data.Event]:
        """ Get events data from StatsBomb """
        return parse.parse_events(
            json=self._adapter.get_events(match_id)
        )

def get_github_repository() -> ReadOnlyRepository:
    return Repository(
        adapter=GithubHTTPSAdapter(),
        serializer=JSONSerializer()
    )

def get_local_repository(base_path) -> ReadOnlyRepository:
    return Repository(
        adapter=LocalAdapter(base_path)
    )

def get_statsbomb_services_repository(username, password) -> ReadOnlyRepository:
    return Repository(
        adapter=StatsbombServicesAdapter(username, password)
    )