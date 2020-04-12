# statsbombapi

*Work in progress*

Dataclasses for Statsbomb data

## What does this package do?

`statsbombapi` aims to make it easier to extract and parse statsbomb data through
the use of dataclasses.

There are some great pre-existing packages for working with statsbomb data:

* https://github.com/statsbomb/statsbombpy
* https://github.com/imrankhan17/statsbomb-parser

However, these are primarily built around fetching Statsbomb data as dataframes.
This is great for interactive work (for example, in a jupyter notebook), but isn't
ideal for [ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load). By parsing
data from the Statsbomb API into specific data structures, this package aims to
make working with Statsbomb data easier.
