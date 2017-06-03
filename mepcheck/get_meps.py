import requests
from bs4 import BeautifulSoup
import pickle

url = "http://www.votewatch.eu//en/term8-european-parliament-members.html?limit=804"

r = requests.get(url)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, "html.parser")
meps = soup.find_all('tr')
countries = soup.find_all('td', class_='margin_image middle_align')

idx = []
i = 0
for mep, country in zip(meps[1:], countries):
    i += 1
    ids = [i, mep.find('div').text.strip().lower(), country.text.strip().lower()]
    idx.append(ids)

with open('meps', 'wb') as f:
    pickle.dump(idx, f, -1)
