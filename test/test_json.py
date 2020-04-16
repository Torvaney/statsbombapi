"""
Test the parsing of (mocked) data from statsbomb API routes
"""
import datetime
import uuid

import hypothesis
import hypothesis.strategies as st

import statsbombapi.json as sb_json
import data


@hypothesis.given(st.text(), st.lists(st.text()), st.lists(st.integers()))
def test_prefix(prefix, ks, vals):
    d = dict(zip(ks, vals))
    assert sb_json.data.remove_prefix(sb_json.data.add_prefix(d, prefix), prefix) == d


def test_extract_unit():
    assert set(sb_json.extract(int, 1)) == {1}
    assert set(sb_json.extract(str, 'a')) == {'a'}

    assert set(sb_json.extract(int, [1, 2, 3])) == {1, 2, 3}
    assert set(sb_json.extract(int, [[5], [4, 3]])) == {3, 4, 5}
    assert set(sb_json.extract(str, ['a', ['b', 'c']])) == {'a', 'b', 'c'}
    assert set(sb_json.extract(bool, [[[[True, False]]]])) == {True, False}

    competition_season = sb_json.CompetitionSeason(
        competition_id=1,
        competition_name='ok',
        competition_gender='female',
        country_name='trytegrw',
        season_id=1,
        season_name='2020/2021',
        match_updated=datetime.datetime(2020, 1, 1),
        match_available=datetime.datetime(2020, 1, 1)
    )
    assert set(sb_json.extract(sb_json.Season, competition_season)) == {sb_json.Season(1, '2020/2021')}
    assert set(sb_json.extract(sb_json.Competition, competition_season)) == {sb_json.Competition(1, 'ok', 'female', 'trytegrw')}


@hypothesis.given(st.lists(st.integers()))
def test_extract_list_ints(xs):
    assert set(sb_json.extract(int, xs)) == set(xs)


@hypothesis.given(st.recursive(st.booleans(), st.lists))
def test_extract_recursive_bool(xs):
    assert ({True, False} | set(sb_json.extract(bool, xs))) == {True, False}


@hypothesis.given(st.recursive(st.builds(sb_json.Season, id=st.integers(), name=st.text()), st.lists))
def test_extract_recursive_json(xs):
    assert all(isinstance(x, sb_json.Season) for x in sb_json.extract(sb_json.Season, xs))


def test_competitions_route():
    competitions = [
        sb_json.Competition(id=3, name="Wessex Women's Championship", gender=sb_json.Gender.FEMALE, country_name='Wessex'),
        sb_json.Competition(id=1, name='Brythonic Premier League', gender=sb_json.Gender.MALE, country_name='Dumnonia'),
        sb_json.Competition(id=2, name="Wessex Men's Championship", gender=sb_json.Gender.MALE, country_name='Wessex'),
    ]

    seasons = [
        sb_json.Season(id=1, name='560/561'),
        sb_json.Season(id=2, name='561/562')
    ]

    for version in ['v2']:
        parsed = sb_json.parse_competitions(data.COMPETITIONS[version])
        assert set(competitions) == set(sb_json.extract(sb_json.Competition, parsed))
        assert set(seasons) == set(sb_json.extract(sb_json.Season, parsed))


def test_matches():
    reference = [
        sb_json.Match(
            id=1234,
            competition=sb_json.Competition(
                id=4, name='League Ān', country_name='Mercia', gender=None
            ),
            season=sb_json.Season(id=3, name='639/640'),
            date=datetime.date(640, 1, 1),
            kick_off=datetime.time(15, 0),
            match_week=35,
            status=sb_json.MatchStatus.SCHEDULED,
            competition_stage=sb_json.CompetitionStage(id=1, name='Regular Season'),
            home_team=sb_json.Team(
                id=101,
                name='Warwick Wanderers',
                gender=sb_json.Gender.MALE,
                country=sb_json.Country(id=3, name='Mercia'),
            ),
            away_team=sb_json.Team(
                id=102,
                name='Tamworth Rovers',
                gender=sb_json.Gender.MALE,
                country=sb_json.Country(id=3, name='Mercia'),
            ),
            home_score=None,
            away_score=None,
            referee=sb_json.Referee(id=123, name='None', country=None),
            metadata=sb_json.MatchMetadata(),
            last_updated=datetime.datetime(2019, 9, 1, 10, 48, 29, 321435),
        ),
        sb_json.Match(
            id=4321,
            competition=sb_json.Competition(
                id=4, name='League Ān', country_name='Mercia', gender=None
            ),
            season=sb_json.Season(id=3, name='655/656'),
            date=datetime.date(655, 10, 15),
            kick_off=datetime.time(18, 0),
            match_week=14,
            status=sb_json.MatchStatus.AVAILABLE,
            competition_stage=sb_json.CompetitionStage(id=1, name='Regular Season'),
            home_team=sb_json.Team(
                id=101,
                name='Warwick Wanderers',
                gender=sb_json.Gender.MALE,
                country=sb_json.Country(id=3, name='Mercia'),
            ),
            away_team=sb_json.Team(
                id=234,
                name='Whitby United',
                gender=sb_json.Gender.MALE,
                country=sb_json.Country(id=4, name='Northumbria'),
            ),
            home_score=1,
            away_score=3,
            referee=sb_json.Referee(
                id=454,
                name='St. Bede',
                country=sb_json.Country(id=4, name='Northumbria'),
            ),
            metadata=sb_json.MatchMetadata(
                data_version='1.1.0', xy_fidelity_version='2', shot_fidelity_version='2'
            ),
            last_updated=datetime.datetime(2020, 2, 11, 11, 18, 7, 21000),
        ),
    ]

    for version in ['v3']:
        assert set(reference) == set(sb_json.parse_matches(data.MATCHES[version]))


def test_lineups():
    teams = [
        sb_json.Team(id=9876, name='Some Home Team', gender=None, country=None),
        sb_json.Team(id=3257463, name='Some Away Team', gender=None, country=None)
    ]
    players = [
        sb_json.Player(
            id=4546,
            name='Some Person',
            birth_date=datetime.date(1992, 1, 1),
            gender=sb_json.Gender.MALE,
            height=173.0,
            weight=63.0,
            country=sb_json.Country(id=11, name='Someplace'),
            nickname=None,
        ),
        sb_json.Player(
            id=6628,
            name='Some Person',
            birth_date=datetime.date(1992, 1, 1),
            gender=sb_json.Gender.MALE,
            height=176.0,
            weight=73.0,
            country=sb_json.Country(id=178, name='Someplace'),
            nickname='Somey',
        ),
        sb_json.Player(
            id=9745,
            name='Some Person',
            birth_date=datetime.date(1993, 1, 1),
            gender=sb_json.Gender.MALE,
            height=172.0,
            weight=73.0,
            country=sb_json.Country(id=11, name='Someplace'),
            nickname='Somey',
        ),
        sb_json.Player(
            id=27341,
            name='Some Person',
            birth_date=datetime.date(1986, 1, 1),
            gender=sb_json.Gender.MALE,
            height=166.0,
            weight=67.0,
            country=sb_json.Country(id=45, name='Someplace'),
            nickname='Somey',
        )
    ]

    for version in ['v2']:
        parsed = sb_json.parse_lineups(data.LINEUPS[version])
        assert set(teams) == set(sb_json.extract(sb_json.Team, parsed))
        assert set(players) == set(sb_json.extract(sb_json.Player, parsed))


def test_events():
    events = [
        sb_json.Event(
            id=uuid.UUID('23c72492-5eb6-4f51-a979-0013304763ba'),
            index=4,
            period=1,
            timestamp=datetime.time(0, 0),
            minute=0,
            second=0,
            type=sb_json.EventType(id=18, name='Half Start'),
            possession=1,
            possession_team=sb_json.Team(id=749, name='Team A', gender=None, country=None),
            play_pattern=sb_json.PlayPattern(id=1, name='Regular Play'),
            team=sb_json.Team(id=749, name='Team A', gender=None, country=None),
            duration=0.0,
            related_events=[uuid.UUID('1757ab8f-bb38-4085-961e-2c417213677f')],
            location=None, under_pressure=None, off_camera=None,
            out=None,
            player=None,
            position=None,
            tactics=None,
            counterpress=None,
            fifty_fifty=None,
            bad_behaviour=None,
            ball_receipt=None,
            ball_recovery=None,
            block=None,
            carry=None,
            clearance=None,
            dribble=None,
            dribbled_past=None,
            duel=None,
            foul_committed=None,
            foul_won=None,
            goalkeeper=None,
            half_end=None,
            half_start=None,
            injury_stoppage=None,
            interception=None,
            miscontrol=None,
            pass_=None,
            player_off=None,
            pressure=None,
            shot=None,
            substitution=None),
        sb_json.Event(
            id=uuid.UUID('b3c89786-8ab7-47ab-9ad8-8a0f60c32507'),
            index=5,
            period=1,
            timestamp=datetime.time(0, 0, 0, 463000),
            minute=0,
            second=0,
            type=sb_json.EventType(id=30, name='Pass'),
            possession=2,
            possession_team=sb_json.Team(id=966, name='Team B', gender=None, country=None),
            play_pattern=sb_json.PlayPattern(id=9, name='From Kick Off'),
            team=sb_json.Team(id=966, name='Team B', gender=None, country=None),
            duration=0.472563,
            related_events=[uuid.UUID('1d63288b-bed3-4d99-aaf0-0e6e9bf82b84')],
            location=[60.0, 40.0],
            under_pressure=None,
            off_camera=None,
            out=None,
            player=sb_json.Player(id=15611, name='Player X', birth_date=None, gender=None, height=None, weight=None, country=None, nickname=None),
            position=sb_json.Position(id=23, name='Center Forward'),
            tactics=None,
            counterpress=None,
            fifty_fifty=None,
            bad_behaviour=None,
            ball_receipt=None,
            ball_recovery=None,
            block=None,
            carry=None,
            clearance=None,
            dribble=None,
            dribbled_past=None,
            duel=None,
            foul_committed=None,
            foul_won=None,
            goalkeeper=None,
            half_end=None,
            half_start=None,
            injury_stoppage=None,
            interception=None,
            miscontrol=None,
            pass_=sb_json.Pass(length=1.4866068, angle=0.8329813, height=sb_json.StatsBombObject(id=1, name='Ground Pass'),
            end_location=[61.0, 41.1],
            recipient=sb_json.Player(id=15547, name='Player Y', birth_date=None, gender=None, height=None, weight=None, country=None, nickname=None),
            body_part=sb_json.StatsBombObject(id=40, name='Right Foot'),
            type=sb_json.StatsBombObject(id=65, name='Kick Off'),
            outcome=None,
            technique=None,
            aerial_won=None,
            assisted_shot_id=None,
            inswinging=None,
            outswinging=None,
            backheel=None,
            deflected=None,
            miscommunication=None,
            cross=None,
            cut_back=None, switch=None, through_ball=None, shot_assist=None, goal_assist=None, xclaim=None), player_off=None, pressure=None, shot=None, substitution=None),
        sb_json.Event(
            id=uuid.UUID('1d63288b-bed3-4d99-aaf0-0e6e9bf82b84'),
            index=6,
            period=1,
            timestamp=datetime.time(0, 0, 0, 936000),
            minute=0,
            second=0,
            type=sb_json.EventType(id=42, name='Ball Receipt*'),
            possession=2,
            possession_team=sb_json.Team(id=966, name='Team B', gender=None, country=None),
            play_pattern=sb_json.PlayPattern(id=9, name='From Kick Off'),
            team=sb_json.Team(id=966, name='Team B', gender=None, country=None),
            duration=None,
            related_events=[uuid.UUID('b3c89786-8ab7-47ab-9ad8-8a0f60c32507')],
            location=[61.0, 41.1],
            under_pressure=None,
            off_camera=None,
            out=None,
            player=sb_json.Player(id=15547, name='Player Y', birth_date=None, gender=None, height=None, weight=None, country=None, nickname=None),
            position=sb_json.Position(id=19, name='Center Attacking Midfield'),
            tactics=None,
            counterpress=None,
            fifty_fifty=None,
            bad_behaviour=None,
            ball_receipt=None,
            ball_recovery=None,
            block=None,
            carry=None,
            clearance=None,
            dribble=None,
            dribbled_past=None,
            duel=None,
            foul_committed=None,
            foul_won=None,
            goalkeeper=None,
            half_end=None,
            half_start=None,
            injury_stoppage=None,
            interception=None,
            miscontrol=None,
            pass_=None,
            player_off=None,
            pressure=None,
            shot=None,
            substitution=None),
        sb_json.Event(
            id=uuid.UUID('21ca17d9-2ba7-4aa5-ae08-bfc82ba6785e'),
            index=7,
            period=1,
            timestamp=datetime.time(0, 0, 0, 936000),
            minute=0,
            second=0,
            type=sb_json.EventType(id=43, name='Carry'),
            possession=2,
            possession_team=sb_json.Team(id=966, name='Team B', gender=None, country=None),
            play_pattern=sb_json.PlayPattern(id=9, name='From Kick Off'),
            team=sb_json.Team(id=966, name='Team B', gender=None, country=None),
            duration=1.418851,
            related_events=[
                uuid.UUID('06ecdc24-c95e-4d5b-80d3-f401568bba3c'),
                uuid.UUID('1d63288b-bed3-4d99-aaf0-0e6e9bf82b84'),
                uuid.UUID('788fccf5-e07f-4902-a22a-f73b89de7e1a')
            ],
            location=[61.0, 41.1],
            under_pressure=True,
            off_camera=None,
            out=None,
            player=sb_json.Player(id=15547, name='Player Y', birth_date=None, gender=None, height=None, weight=None, country=None, nickname=None),
            position=sb_json.Position(id=19, name='Center Attacking Midfield'),
            tactics=None,
            counterpress=None,
            fifty_fifty=None,
            bad_behaviour=None,
            ball_receipt=None,
            ball_recovery=None,
            block=None,
            carry=sb_json.Carry(end_location=[63.4, 35.0]),
            clearance=None,
            dribble=None,
            dribbled_past=None,
            duel=None,
            foul_committed=None,
            foul_won=None,
            goalkeeper=None,
            half_end=None,
            half_start=None,
            injury_stoppage=None,
            interception=None,
            miscontrol=None,
            pass_=None,
            player_off=None,
            pressure=None,
            shot=None,
            substitution=None),
    ]

    for version in ['v5']:
        parsed = sb_json.parse_events(data.EVENTS[version])
        assert events == list(parsed)
