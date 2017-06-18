import pytest

from mepcheck import EUvotes, get_meps
from mepcheck.savemeps import save_meps

import requests
from bs4 import BeautifulSoup
import pickle
import os
from datetime import date, timedelta
import json
import pandas as pd


def test_save_meps():
    save_meps()
    assert os.path.isfile(os.path.expanduser("~/.meps"))

def test_EUvotes():
    eu = EUvotes(1, limit=10)
    assert eu.limit == 10

def test_mep_name():
    assert EUvotes(1, limit=1).name == EUvotes(1, limit=1)._mep_name(1)

def test_get_votes():
    assert len(EUvotes(1, limit=10).absent) == 10

def test_to_date():
    assert isinstance(EUvotes(1, limit=1)._to_date("2017-01-01"), date)

def test_last_vote_period():
    votes = EUvotes(1, limit=1)
    dates = [date.today(),
             date.today() - timedelta(weeks=1),
             date.today() - timedelta(weeks=4),
             date.today() - timedelta(weeks=52)]
    assert votes._last_vote_period(dates) == [
        "This week",
        "This month",
        "More than one month",
        "More than one month"
    ]

def test_change_limit():
    lim = EUvotes(1, 1)
    lim_before = lim.limit
    lim.change_limit(5)
    assert lim_before != lim.limit

def test_data_():
    data = EUvotes(1, 2)
    assert isinstance(data.data_("json"), str) and isinstance(data.data_("list"), list) and isinstance(data.data_("df"), pd.DataFrame)
