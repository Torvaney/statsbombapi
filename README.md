# statsbombapi

API wrapper and dataclasses for StatsBomb data

## Installation

To get the latest version from GitHub:

``` bash
pip install git+https://github.com/torvaney/statsbombapi.git
```

## Getting started

``` python
>>> import statsbombapi

# Connect to the Public Data Repo
>>> api = statsbombapi.StatsBombPublic()
UserWarning: Please be responsible with StatsBomb data and make sure you have
 registered your details on https://www.statsbomb.com/resource-centre, and read and
 accepted the User Agreement (available on the same page).
  warnings.warn(statsbomb_data_advice)

# Or, if connecting to the API proper
>>> api = statsbombapi.StatsBombAPI(username='...', password='...')
```

The StatsBomb API provides 4 routes, which can be accessed by calling the
corresponding methods on `StatsBombPublic` or `StatsBombAPI`.

* competitions - `api.competitions()`
* matches - `api.matches(competition_id, season_id)`
* lineups - `api.lineups(match_id)`
* events - `api.events(match_id)`

### Competitions

``` python
>>> competitions = api.competitions()
>>> competitions[0].competition
Competition(id=37, name="FA Women's Super League", gender=<Gender.FEMALE: 'female'>, country_name='England')

>>> competitions[0].season
Season(id=42, name='2019/2020')

>>> competitions[0].match_updated, competitions[0].match_available
(datetime.datetime(2020, 3, 11, 14, 9, 41, 932138),
 datetime.datetime(2020, 3, 11, 14, 9, 41, 932138))

>>> # Or extract individual objects from the API response
>>> set(statsbombapi.extract(statsbombapi.Competition, competitions))
{Competition(id=11, name='La Liga', gender=<Gender.MALE: 'male'>, country_name='Spain'),
 Competition(id=37, name="FA Women's Super League", gender=<Gender.FEMALE: 'female'>, country_name='England'),
 Competition(id=43, name='FIFA World Cup', gender=<Gender.MALE: 'male'>, country_name='International'),
 Competition(id=49, name='NWSL', gender=<Gender.FEMALE: 'female'>, country_name='United States of America'),
 Competition(id=72, name="Women's World Cup", gender=<Gender.FEMALE: 'female'>, country_name='International')}

>>> set(statsbombapi.extract(statsbombapi.Season, competitions))
{Season(id=1, name='2017/2018'),
 Season(id=2, name='2016/2017'),
 Season(id=21, name='2009/2010'),
 Season(id=22, name='2010/2011'),
 Season(id=23, name='2011/2012'),
 Season(id=24, name='2012/2013'),
 Season(id=25, name='2013/2014'),
 Season(id=26, name='2014/2015'),
 Season(id=27, name='2015/2016'),
 Season(id=3, name='2018'),
 Season(id=30, name='2019'),
 Season(id=37, name='2004/2005'),
 Season(id=38, name='2005/2006'),
 Season(id=39, name='2006/2007'),
 Season(id=4, name='2018/2019'),
 Season(id=40, name='2007/2008'),
 Season(id=41, name='2008/2009'),
 Season(id=42, name='2019/2020')}
```

### Matches

``` python
>>> matches = api.matches(competition_id=37, season_id=42)

>>> # You can use the `extract` function to find items of any relevant type,
>>> # even if they are nested to arbitrary depth
>>> teams = set(statsbombapi.extract(statsbombapi.Team, matches))
>>> countries = set(statsbombapi.extract(statsbombapi.Country, matches))
>>> referees = set(statsbombapi.extract(statsbombapi.Referee, matches))
```

### Lineups

``` python
>>> lineups = api.lineups(match_id=2275086)

>>> # Same as before...
>>> players = set(statsbombapi.extract(statsbombapi.Player, lineups))
>>> list(players)[0]
Player(id=15616, name='Kim Little', birth_date=None, gender=None, height=None, weight=None,
 country=Country(id=201, name='Scotland'), nickname=None)
```

### Events

``` python
>>> # Last, but certainly not least
>>> events = api.events(match_id=2275086)
>>> events[224]
Event(id=UUID('8b7f985e-2fa5-4b08-9893-0d1b77cf7076'), index=225, period=1,
 timestamp=datetime.time(0, 4, 35, 263000), minute=4, second=35,
 type=EventType(id=43, name='Carry'), possession=13,
 possession_team=Team(id=968, name='Arsenal WFC', gender=None, country=None),
 play_pattern=PlayPattern(id=4, name='From Throw In'),
 team=Team(id=968, name='Arsenal WFC', gender=None, country=None),
 duration=0.444403, related_events=[UUID('7eed3cb4-b02c-4ddb-bb98-1526cd4c89d5'), UUID('8af13ea5-1b32-4ea2-91fd-93756979744d')],
 location=[28.6, 20.8], under_pressure=None, off_camera=None, out=None,
 player=Player(id=10405, name='Lia Wälti', birth_date=None, gender=None, height=None, weight=None, country=None, nickname=None),
 position=Position(id=2, name='Right Back'), tactics=None, counterpress=None,
 fifty_fifty=None, bad_behaviour=None, ball_receipt=None, ball_recovery=None,
 block=None, carry=Carry(end_location=[28.6, 20.8]), clearance=None, dribble=None,
 dribbled_past=None, duel=None, foul_committed=None, foul_won=None, goalkeeper=None,
 half_end=None, half_start=None, injury_stoppage=None, interception=None,
 miscontrol=None, pass_=None, player_off=None, pressure=None, shot=None, substitution=None)
```

## Other output formats

If you don't want to use dataclasses, `statsbombapi` provides an extensible API client
to enable you to fetch StatsBomb data in whatever format you want.

### Loaders and Decoders

The API Client is composed of a loader and a decoder:

```python
client = statsbombapi.StatsbombPublic()

# Is equivalent to
client = statsbombapi.APIClient(
  loader=statsbombapi.loaders.OpenDataLoader(),
  decoder=statsbombapi.decoders.DataclassDecoder()
)
```

Alternative decoders can be used to return data in a different format:

```python
json_client = statsbombapi.APIClient(
  loader=statsbombapi.loaders.OpenDataLoader(),
  decoder=statsbombapi.decoders.JsonDecoder()
)

# You can also supply the decoder to the pre-defined clients
json_client = statsbombapi.StatsbombPublic(
  decoder=statsbombapi.decoders.JsonDecoder()
)

json_client = statsbombapi.StatsbombAPI(
  username='...',
  password='...',
  decoder=statsbombapi.decoders.JsonDecoder()
)
```

You could use this interface to use own custom decoders. For example,
you might want to return data as pandas DataFrames:

```python
import pandas as pd

dataframe_decoder = statsbombapi.decoders.CompositeDecoder(
  # The default loader returns the object as bytes, so we need
  # to chain together two decoders using `CompositeDecoder`.
  # The first (`JsonDecoder`) uses json.decode to decode the API response into
  # Python objects (lists and dicts)
  statsbombapi.decoders.JsonDecoder,
  # The second uses the `pd.DataFrame` constructor on the output of 4 API routes
  # (after they've been decoded by `JsonDecoder`)
  statsbombapi.decoders.UniformDecoder(pd.DataFrame)
)

df_client = statsbombapi.StatsbombPublic(
  decoder=dataframe_decoder
)

>>> print(df_client.events(match_id=2275086))
                                        id  index  period     timestamp  minute  second  ...
0     098da6e7-be60-4e70-8567-916873b0ba15      1       1  00:00:00.000       0       0  ...
1     7ef1ced6-7044-4788-a7b7-d9d669071ecd      2       1  00:00:00.000       0       0  ...
2     9e1da46b-dccc-4382-9603-d1fc1203b041      3       1  00:00:00.000       0       0  ...
3     a5f24a50-053f-4c18-920d-5e70471e31c4      4       1  00:00:00.000       0       0  ...
4     b3394890-ef26-4709-b00c-bcba2985a4cc      5       1  00:00:00.512       0       0  ...
...                                    ...    ...     ...           ...     ...     ...  ...
3260  0623b1ff-742e-4ee7-9c85-f27bee25c761   3261       2  00:49:32.803      94      32  ...
3261  69ab6703-a024-44b9-9883-05b19586be86   3262       2  00:49:32.930      94      32  ...
3262  34f79b82-e513-4ab5-9393-9f4e223f7ed4   3263       2  00:49:33.326      94      33  ...
3263  a3907011-3386-4578-a910-51cfa5bb5773   3264       2  00:49:33.738      94      33  ...
3264  70f30ecb-b85d-48d9-83bc-f62e1613dc3f   3265       2  00:49:33.738      94      33  ...
```

Likewise, you could swap out the loader to load from disk (`statsbombapi.LocalLoader`),
or define a custom loaders to (for example) cache data locally, or pull data from s3.


## Yet another statsbomb API package?!

Yes! `statsbombapi` aims to make it easier to extract and parse statsbomb
data with the use of dataclasses.

There are some great pre-existing packages for working with statsbomb data:

* https://github.com/statsbomb/statsbombpy
* https://github.com/imrankhan17/statsbomb-parser

These are primarily built around fetching StatsBomb data as dataframes.
This is great for interactive work (for example, in a jupyter notebook) and you
should definitely consider whether they match your use-case.

However, I have found that this approach sometimes isn't ideal when developing data pipelines
and doing ETL. By parsing data from the StatsBomb API into specific data structures,
I hope that this package can make these situations easier.

## Development

### Testing

Run tests with `pytest test`.
