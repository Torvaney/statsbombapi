from . import loaders, decoders


class APIClient:
    def __init__(self, loader, decoder):
        self.loader = loader
        self.decoder = decoder

    def competitions(self):
        return self.decoder.decode_competitions(
            self.loader.load_competitions()
        )

    def matches(self, competition_id, season_id):
        return self.decoder.decode_matches(
            self.loader.load_matches(competition_id, season_id)
        )

    def lineups(self, match_id):
        return self.decoder.decode_lineups(
            self.loader.load_lineups(match_id)
        )

    def events(self, match_id):
        return self.decoder.decode_events(
            self.loader.load_events(match_id)
        )


class StatsbombPublic(APIClient):
    def __init__(self, decoder=decoders.DataclassDecoder()):
        self.loader = loaders.OpenDataLoader()
        self.decoder = decoder


class StatsbombAPI(APIClient):
    def __init__(self, username, password, decoder=decoders.DataclassDecoder()):
        self.loader = loaders.StatsbombAPILoader(
            username=username,
            password=password
        )
        self.decoder = decoder
