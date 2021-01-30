import requests
import json
from bs4 import BeautifulSoup
import sys, argparse

"""
parser = argparse.ArgumentParser(description='Get heroes that are countered and counter your hero.')
parser.add_argument('--hero', help='The name of your hero. Case insensitve.',type=str)
parser.add_argument('--timeframe','-tf', help='The timeframe for data. 1 = 1wk, 2 = 1mo, 3 = 3mo, 4 = 6mo, 5 = 1yr. default=5',type=int,default=5)

args = parser.parse_args()
"""

#Get heroes
URL = 'https://api.opendota.com/api/heroes'
response = requests.get(URL)
heroes = response.json()

#vars
"""
hero = 0
date = args['timeframe']
dates = ['week','month','3month','6month','year']
"""
hero = ''
date = -1
exists = -1
dates = ['week','month','3month','6month','year']

#get valid hero input
while exists == -1:
    hero = input('Name of your hero: ').lower()
    for dict in heroes:
        if dict['localized_name'].lower() == hero:
            exists = 1

hero = hero.replace(' ','-')

#get valid time range
while date < 1 or date > 5:
    date = int(input('Select a time range for data:\n1. week\n2. month\n3. 3 months\n4. 6 months\n5. year\n'))
print()

#WEB SCRAPING
#request to dotabuff
URL = 'https://www.dotabuff.com/heroes/' + hero + '/counters?date=' + dates[date - 1]
headers = {
    'User-Agent':'Mozilla/5.0'
}
page = requests.get(URL,headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

#grab sections
content = soup.find_all('section', class_='counter-outline')

td_arr = []

#for each section
for elem in content:
    #get the header text
    header = elem.find('header')
    print(header.text.upper(), end = '\n')

    col_headers = elem.find_all('th')
    for th in col_headers:
        print('{0:20s}'.format(th.text), end = '')

    print()
    print('-' * 60)

    #get all the rows
    table = elem.find('tbody')
    rows = table.find_all('tr')
    #for each tr
    for tr in rows:
        #find all td
        td = tr.find_all('td')
        #for each td
        for value in td:
            td_arr.append(value.text)
        print('{0:20s}{1:20s}{2:20s}'.format(td_arr[1],td_arr[2],td_arr[3]), end = '\n'*2)
        td_arr.clear()