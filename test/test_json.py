"""
Test the parsing of (mocked) data from statsbomb API routes
"""
import datetime

import statsbombapi
import data


def test_competitions():
    reference = [
        (statsbombapi.Competition(id=1, name='Brythonic Premier League', country_name='Dumnonia', gender=statsbombapi.Gender.MALE),
         statsbombapi.Season(id=1, name='560/561')),
        (statsbombapi.Competition(id=1, name='Brythonic Premier League', country_name='Dumnonia', gender=statsbombapi.Gender.MALE),
         statsbombapi.Season(id=2, name='561/562')),
        (statsbombapi.Competition(id=2, name="Wessex Men's Championship", country_name='Wessex', gender=statsbombapi.Gender.MALE),
         statsbombapi.Season(id=2, name='561/562')),
        (statsbombapi.Competition(id=3, name="Wessex Women's Championship", country_name='Wessex', gender=statsbombapi.Gender.FEMALE),
         statsbombapi.Season(id=2, name='561/562'))
    ]

    for version in ['v2']:
        assert set(reference) == set(statsbombapi.parse_competitions(data.COMPETITIONS[version]))


def test_matches():
    reference = [
        Match(id=1234,
              competition=Competition(id=4, name='League Ān', country_name='Mercia', gender=None),
              season=Season(id=3, name='639/640'), date=datetime.date(640, 1, 1),
              kick_off=datetime.time(15, 0), match_week=35,
              status=statsbombapi.MatchStatus.SCHEDULED,
              competition_stage=CompetitionStage(id=1, name='Regular Season'),
              home_team=Team(id=101, name='Warwick Wanderers', gender=None, country=Country(id=3, name='Mercia')),
              away_team=Team(id=102, name='Tamworth Rovers', gender=None, country=Country(id=3, name='Mercia')),
              home_score=None,
              away_score=None,
              referee=Referee(id=123, name='None', country=None),
              last_updated=datetime.datetime(2019, 9, 1, 10, 48, 29, 321435)),
        Match(id=4321,
              competition=Competition(id=4, name='League Ān', country_name='Mercia', gender=None),
              season=Season(id=3, name='655/656'),
              date=datetime.date(655, 10, 15),
              kick_off=datetime.time(18, 0),
              match_week=14,
              status=statsbombapi.MatchStatus.AVAILABLE,
              competition_stage=CompetitionStage(id=1, name='Regular Season'),
              home_team=Team(id=101, name='Warwick Wanderers', gender=None, country=Country(id=3, name='Mercia')),
              away_team=Team(id=234, name='Whitby United', gender=None, country=Country(id=4, name='Northumbria')),
              home_score=1,
              away_score=3,
              referee=Referee(id=454, name='St. Bede', country=Country(id=4, name='Northumbria')),
              last_updated=datetime.datetime(2020, 2, 11, 11, 18,7, 21000))
    ]

    for version in ['v3']:
        assert set(reference) == set(statsbombapi.parse_matches(data.MATCHES[version]))
