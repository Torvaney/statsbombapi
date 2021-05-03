import functools
import json

from .json import parse


class UniformDecoder:
    def __init__(self, decode):
        self.decode = decode

    def decode_competitions(self, s):
        return self.decode(s)

    def decode_matches(self, s):
        return self.decode(s)

    def decode_lineups(self, s):
        return self.decode(s)

    def decode_events(self, s):
        return self.decode(s)


class JsonDecoder(UniformDecoder):
    def __init__(self):
        self.decode = json.loads


class BaseDataclassDecoder:
    def decode_competitions(self, s):
        return parse.parse_competitions(s)

    def decode_matches(self, s):
        return parse.parse_matches(s)

    def decode_lineups(self, s):
        return parse.parse_lineups(s)

    def decode_events(self, s):
        return parse.parse_events(s)


class CompositeDecoder:
    def __init__(self, *decoders):
        # Use a tuple for that sweet, sweet immutability
        self.decoders = tuple(decoders)

    def _decode(self, attr, s=None):
        decoder_funcs = [getattr(d, attr) for d in self.decoders]
        return functools.reduce(lambda x, f: f(x), decoder_funcs, s)

    def decode_competitions(self, s):
        return self._decode('decode_competitions', s)

    def decode_matches(self, s):
        return self._decode('decode_matches', s)

    def decode_lineups(self, s):
        return self._decode('decode_lineups', s)

    def decode_events(self, s):
        return self._decode('decode_events', s)


class DataclassDecoder(CompositeDecoder):
    def __init__(self):
        self.decoders = (JsonDecoder(), BaseDataclassDecoder())
