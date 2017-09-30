#!/usr/bin/env python3

from collections import Counter
from datetime import date, timedelta
import itertools
import json
import pickle
from prettytable import PrettyTable
import requests
import os
from .savemeps import save_meps

url = 'http://www.votewatch.eu/actions.php?euro_parlamentar_id={}&form_category=get_mep_acte&sEcho=1&iColumns=6&sColumns=&iDisplayStart=0&iDisplayLength={}&mDataProp_0=mysql_data&mDataProp_1=act_nume_full&mDataProp_2=euro_vot_valoare_special_vote_page&mDataProp_3=euro_vot_rol_euro_grup.rol_af&mDataProp_4=euro_domeniu_nume&mDataProp_5=euro_vot_valoare_text&sSearch=&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch_3=&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&sSearch_5=&bRegex_5=false&bSearchable_5=true&iSortingCols=1&iSortCol_0=0&sSortDir_0=desc&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=true&bSortable_4=true&bSortable_5=true&_=1486840527483'

def get_meps(country=None):
    """Reference list of countries and MEPs and their ids
    for data retrieval.

    Parameters
    -----------
    country: str
        If None as per default prints a list of available
        countries, otherwise prints a list of MEPs of the
        given country.

    """
    meps_path = os.path.expanduser("~/.meps")
    if os.path.isfile(meps_path):
        with open(meps_path, 'rb') as f:
            meps = pickle.load(f)
        if country is not None:
            t = PrettyTable(['ID', 'Name', 'Country'])
            for mep in meps:
                if mep[2] == country.lower():
                    t.add_row([mep[0], mep[1].title(), mep[2].title()])
            print(t)
        else:
            print("\nSearch through these countries:\n")
            countries = []
            for mep in meps:
                countries.append(mep[2])
            countries = set(countries)
            t = PrettyTable(['Country'])
            for country in countries:
                t.add_row([country.title()])
            print(t)
    else:
        save_meps()
        get_meps(country)

class EUvotes(object):
    """Retrieve MEP last votes from VoteWatch.eu,
    print them in tabular format and summarize them.
    It is possible to return None by printing via
    stdout or to return results in various formats for
    various uses.

    Parameters
    -----------
    mep_id: int
        The id of the MEP you want to check. To see a list
        of MEPs and their ids use get_meps(country)
    limit: int
        The number of votes you want to check, default
        is 50

    """

    def __init__(self, mep_id, limit=50):
        """When launching initialization use given data
        to retrieve all interesting info from Votewatch.eu
        automatically.
        """
        self.mep_id = abs(mep_id)
        self.limit = abs(limit)
        self.dates, self.domains, self.absent = self._get_votes(self.mep_id, self.limit)
        self.dates = self._convert_to_date(self.dates)
        self.period = self._last_vote_period(self.dates)
        self.name = self._mep_name(self.mep_id)

    def __str__(self):
        printing = ("Data about last {} votes for {}".format(self.limit, self.name) + "\n\nTo see the data use `print_attendance` method, `summary=True` prints only a summary of votes")
        return printing

    def _mep_name(self, mep_id):
        """Get searched MEP name"""
        meps_path = os.path.expanduser("~/.meps")
        if os.path.isfile(meps_path):
            with open(os.path.expanduser(meps_path), 'rb') as f:
                meps = pickle.load(f)
            return meps[abs(mep_id) - 1][1]
        else:
            save_meps()
            self._mep_name(mep_id)

    def _get_votes(self, mep_id, limit):
        """Get last `limit` votes for requested MEP"""
        r = requests.get(url.format(abs(mep_id), abs(limit)))
        data = json.loads(r.text)
        dates = [vote['mysql_data_text'] for vote in data['all_votes']]
        domains = [domain['euro_domeniu_nume'] for domain in data['all_votes']]
        absent = [vote['euro_vot_rol_euro_grup']['rol_af'] for vote in data['all_votes']]
        for i, vote in enumerate(absent):
            if vote == "Didn&#39;t vote":
                absent[i] = "Absent"
        return dates, domains, absent

    def _to_date(self, dates):
        """Helper method to convert str to dates"""
        y, m, d = dates.split('-')
        return date(int(y), int(m), int(d))

    def _convert_to_date(self, dates):
        """Convert retrieved str dates to date objects"""
        return [self._to_date(date) for date in dates]

    def _last_vote_period(self, dates):
        """Transform dates to three reference periods"""
        vote_period = []
        for vote in dates:
            period = date.today() - vote
            if period < timedelta(weeks=1):
                vote_period.append("This week")
            elif period < timedelta(weeks=4):
                vote_period.append("This month")
            else:
                vote_period.append("More than one month")
        return vote_period

    def change_limit(self, limit=50):
        print("Updating limit from {} to {}".format(self.limit, abs(limit)))
        self.__init__(self.mep_id, abs(limit))

    def print_attendance(self, summary=False):
        """Print retrieved data to stdout in a nice tabular
        format.

        Parameters
        -----------
        summary: bool
            If True prints a count of votes by tipology and
            period of time.

        Return
        --------
        None

        """
        if summary:
            counts = Counter(zip(self.period, self.absent))
            t = PrettyTable(['Period', 'Vote', 'Count'])
            periods = ["This week", "This month", "More than one month"]
            voting = ["Absent", "Loyal", "Rebel", "No political line"]
            for per in [(i, j) for i in periods for j in voting]:
                t.add_row([per[0], per[1], counts[per]])
            print("\nCount of last {} votes by period for {}. Percentage of absenteeism: {:.1%}\n".format(
                  self.limit, self.name.title(), Counter(self.absent)[voting[0]] / self.limit))
            print(t)
        else:
            print("Last {} votes attendance for {}".format(self.limit, self.name.title()))
            t = PrettyTable(['Date', 'Vote', 'Topic'])
            for row in zip(self.dates, self.absent, self.domains):
                t.add_row(row)
            print(t)

    def data_(self, shape='json', limit=50):
        """Return retrieved data in various formats for
        various possible uses.

        Parameters
        -----------
        shape: ['json', 'list', 'df']
            Decide the format of the returned data.
        limit: int
            Get only last x votes retrieved, default is 50.


        Return
        -------
        json, list or DataFrame depending on `shape` parameter

        """
        if shape == 'json':
            js = []
            for day, presence, topic in zip(self.dates[:limit], self.absent[:limit], self.domains[:limit]):
                js.append({'Date': day.isoformat(), 'Vote': presence, 'Topic': topic})
            return json.dumps(js)
        elif shape == 'list':
            ls = []
            for day, presence, topic in zip(self.dates[:limit], self.absent[:limit], self.domains[:limit]):
                ls.append([day.isoformat(), presence, topic])
            return ls
        elif shape == 'df':
            import pandas as pd
            df = pd.DataFrame({'Date': self.dates[:limit], 'Vote': self.absent[:limit], 'Topic': self.domains[:limit]})
            return df
        else:
            raise NameError("`shape` argument must be 'json', 'list' or 'df'")


if __name__ == '__main__':
    import mepcheck_cli
    mepcheck_cli.cli()
