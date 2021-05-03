"""
Test the parsing of real data from statsbomb's opendata repo
NOTE: requires an internet connection!
"""
import statsbombapi
import warnings


def _test_route(route, *args, **kwargs):
    s = statsbombapi.APIClient(
        loader=statsbombapi.loaders.OpenDataLoader(),
        decoder=None
    )

    decoders = [
        statsbombapi.decoders.JsonDecoder(),
        statsbombapi.decoders.DataclassDecoder()
    ]
    for decoder in decoders:
        s.decoder = decoder
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            getattr(s, route)(*args, **kwargs)


def test_competitions():
    _test_route('competitions')


def test_matches():
    _test_route('matches', 16, 4)


def test_lineups():
    _test_route('lineups', 22912)


def test_events():
    _test_route('events', 22912)
