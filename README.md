![alt text](http://i.imgur.com/0WoVJru.png "MEPcheck")

[![Build Status](https://travis-ci.org/alanmarazzi/mepcheck.svg?branch=master)](https://travis-ci.org/alanmarazzi/mepcheck) [![codebeat badge](https://codebeat.co/badges/ef1d1338-e6de-49b5-b1d6-da0cba215da9)](https://codebeat.co/projects/github-com-alanmarazzi-mepcheck-master) [![codecov](https://codecov.io/gh/alanmarazzi/mepcheck/branch/master/graph/badge.svg)](https://codecov.io/gh/alanmarazzi/mepcheck) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# What is it

**MEPcheck** is a Python package for easy and automatic retrieval of voting data about MEPs (Members of European Parliament). Many people complain they don't know what the EU is doing and especially what MEPs from their country are doing. Take control of your representatives and easily show others what's happening in Brussels/Strasbourg!

# Try it

To try MEPcheck just clone this repo (pip package coming soon):

```bash
git clone https://github.com/alanmarazzi/mepcheck.git
```

Then you can install it as a regular package after installing dependencies:

```bash
cd mepcheck
pip install -r requirements.txt
pip install .
```

# Command Line Interface

After installing you can use **MEPcheck** directly from the command line with

```bash
python mepcheck.py # prints available countries
python mepcheck.py -c spain # prints MEPs from inserted country and their ids
python mepcheck.py --mep 123 # see last 50 votes of a MEP
python mepcheck.py --mep 123 --limit 10 # limit to last 10 votes
python mepcheck.py --mep 123 -s # get a summary by time frame
```

# From Python

You can import the `mepcheck` module in Python and use it interactively or programmatically:

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

To use data you can return all retrieved data in various formats: *json*, *list* or if you like in a [pandas](http://pandas.pydata.org/) *DataFrame*:

```python
votes.data_(shape='list', limit=10)
```

Note that if you want *DataFrame* you have to install pandas since it is not a requirement.

# Docker

If you want **MEPcheck** to work out of the box and use it from everywhere without messing with your *PATH*, just build it with *Docker*.

The process is:

```bash
cd mepcheck
docker build -t mepcheck .
```

Then just put in your `.bashrc` file:

```bash
alias mepcheck='sudo docker run --rm mepcheck'
```

Now either you `source ~/.bashrc` or close and reopen your terminal, at this point you can try it with:

```bash
mepcheck --mep 123
```

# Contributing

I'm open to any kind of contribution: ideas, pull requests and bug signaling are welcome.

## Thanks to

- [logomakr](https://logomakr.com/)
- [Votewatch](http://www.votewatch.eu/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [requests](http://docs.python-requests.org/en/master/)
- [prettytable](https://pypi.python.org/pypi/PrettyTable)
