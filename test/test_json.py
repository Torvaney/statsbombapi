import statsbombapi

def test_competition():
    reference = statsbombapi.Competition(
        id=1,
        name='Division 1',
        country_name='Genovia',
        gender=statsbombapi.Gender.MALE
    )

    tested = statsbombapi.Competition.from_json(
        '{"competition_id": 1, "country_name": "Genovia", "competition_name": "Division 1", "gender": "male"}'
    )

    assert reference == tested


def test_season():
    reference = statsbombapi.Season(
        id=1,
        name='1066/1067'
    )

    tested = statsbombapi.Season.from_json(
        '{"season_id": 1, "season_name": "1066/1067"}'
    )

    assert reference == tested


def test_match():
    reference = statsbombapi.Match(
        id=1,
        competition=statsbombapi.Competition(
            id=1,
            name='Division 1',
            country_name='Genovia',
            gender=statsbombapi.Gender.MALE
        )
    )

    tested = statsbombapi.Match.from_json(
        '{"match_id": 1, "competition": {"competition_id": 1, "country_name": "Genovia", "competition_name": "Division 1", "gender": "male"}}'
    )

    assert reference == tested
