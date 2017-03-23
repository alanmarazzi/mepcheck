![alt text](http://i.imgur.com/0WoVJru.png "MEPcheck")

# Work in progress

This will become a Python package for easy and automatic retrieval of voting data about MEPs (Members of European Parliament).

To see what's going on at the moment you can check the [**TODO**](https://github.com/alanmarazzi/mepcheck/blob/master/TODO.md) in this repo.

# Try it

To try MEPcheck just clone this repo:

```bash
git clone http://etc
```

Then you can import the module from repo's folder:

```bash
cd mepcheck
python
```
```python
from mepcheck import EUvotes, get_meps
```

Now you can start retrieving data for all MEPs from [Votewatch](http://www.votewatch.eu/), to check all MEPS and their ids use `get_meps`: if you don't pass any argument you'll get a list of all available countries, if you pass a country you'll get a table with all the MEPs from that country and their id for data retrieval:

```python
get_meps()
get_meps(country='latvia')
```

To get data use the `EUvotes` class, you can just pass the id of the MEP you're interested in and then you can take a look at the data right away:

```python
votes = EUvotes(123, limit=20)
print(votes)
votes.print_attendance(summary=True)
```

To use data you can return all retrieved data in various formats: *json*, *list* or if you like in a [pandas](link_to_pandas) *DataFrame*:

```python
votes.data_(shape='list', limit=10)
```

# Contributing

I'm open to any kind of contribution: ideas, pull requests and bug signaling are welcome.

## Thanks to

- [logomakr](https://logomakr.com/)
- [Votewatch](http://www.votewatch.eu/)
