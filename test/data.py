COMPETITIONS = {
    "v2": [
        {
            "competition_id": 1,
            "season_id": 1,
            "country_name": "Dumnonia",
            "competition_name": "Brythonic Premier League",
            "competition_gender": "male",
            "season_name": "560/561",
            "match_updated": "2020-01-30T02:24:23.296715",
            "match_available": "2020-01-30T02:24:23.296715",
        },
        {
            "competition_id": 1,
            "season_id": 2,
            "country_name": "Dumnonia",
            "competition_name": "Brythonic Premier League",
            "competition_gender": "male",
            "season_name": "561/562",
            "match_updated": "2000-12-01T23:00:00.000000",
            "match_available": "2000-12-01T23:00:00.000000",
        },
        {
            "competition_id": 2,
            "season_id": 2,
            "country_name": "Wessex",
            "competition_name": "Wessex Men's Championship",
            "competition_gender": "male",
            "season_name": "561/562",
            "match_updated": "2000-12-01T23:00:00.000000",
            "match_available": "2000-12-01T23:00:00.000000",
        },
        {
            "competition_id": 3,
            "season_id": 2,
            "country_name": "Wessex",
            "competition_name": "Wessex Women's Championship",
            "competition_gender": "female",
            "season_name": "561/562",
            "match_updated": "2000-12-01T23:00:00.000000",
            "match_available": "2000-12-01T23:00:00.000000",
        },
    ]
}


MATCHES = {
    "v3": [
        {
            "match_id": 1234,
            "match_date": "0640-01-01",
            "kick_off": "15:00:00.000",
            "competition": {
                "competition_id": 4,
                "country_name": "Mercia",
                "competition_name": "League Ān",
            },
            "season": {"season_id": 3, "season_name": "639/640"},
            "home_team": {
                "home_team_id": 101,
                "home_team_name": "Warwick Wanderers",
                "home_team_gender": "male",
                "home_team_group": None,
                "country": {"id": 3, "name": "Mercia"},
            },
            "away_team": {
                "away_team_id": 102,
                "away_team_name": "Tamworth Rovers",
                "away_team_gender": "male",
                "away_team_group": None,
                "country": {"id": 3, "name": "Mercia"},
            },
            "home_score": None,
            "away_score": None,
            "match_status": "scheduled",
            "last_updated": "2019-09-01T10:48:29.321435",
            "metadata": {},
            "match_week": 35,
            "competition_stage": {"id": 1, "name": "Regular Season"},
            "stadium": {
                "id": 383,
                "name": "Eastgate",
                "country": {"id": 3, "name": "Mercia"},
            },
            "referee": {"id": 123, "name": "None"},
        },
        {
            "match_id": 4321,
            "match_date": "0655-10-15",
            "kick_off": "18:00:00.000",
            "competition": {
                "competition_id": 4,
                "country_name": "Mercia",
                "competition_name": "League Ān",
            },
            "season": {"season_id": 3, "season_name": "655/656"},
            "home_team": {
                "home_team_id": 101,
                "home_team_name": "Warwick Wanderers",
                "home_team_gender": "male",
                "home_team_group": None,
                "country": {"id": 3, "name": "Mercia"},
                "managers": [
                    {
                        "id": 345,
                        "name": "Penda Pybbasen",
                        "nickname": None,
                        "dob": "626-04-01",
                        "country": {"id": 3, "name": "Mercia"},
                    },
                    {
                        "id": 546,
                        "name": "Æthelhere Wuffingas",
                        "nickname": None,
                        "dob": "0627-04-01",
                        "country": {"id": 3, "name": "East Anglia"},
                    }
                ],
            },
            "away_team": {
                "away_team_id": 234,
                "away_team_name": "Whitby United",
                "away_team_gender": "male",
                "away_team_group": None,
                "country": {"id": 4, "name": "Northumbria"},
                "managers": [
                    {
                        "id": 546,
                        "name": "Oswiu, son of Æthelfrith",
                        "nickname": "Oswig",
                        "dob": "0612-02-12",
                        "country": {"id": 4, "name": "Northumbria"},
                    }
                ],
            },
            "home_score": 1,
            "away_score": 3,
            "match_status": "available",
            "last_updated": "2020-02-11T11:18:07.021",
            "metadata": {
                "data_version": "1.1.0",
                "shot_fidelity_version": "2",
                "xy_fidelity_version": "2",
            },
            "match_week": 14,
            "competition_stage": {"id": 1, "name": "Regular Season"},
            "stadium": {
                "id": 234,
                "name": "Cock Beck",
                "country": {"id": 3, "name": "Mercia"},
            },
            "referee": {
                "id": 454,
                "name": "St. Bede",
                "country": {"id": 4, "name": "Northumbria"},
            },
        },
    ]
}
