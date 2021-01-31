import requests
import json
from bs4 import BeautifulSoup

def getHeroData(hero,date):
    #vars
    dates = ['week','month','3month','6month','year']

    #templar assassin -> templar-assasin
    heroLookup = hero.replace(' ','-')

    #WEB SCRAPING
    #request to dotabuff
    URL = 'https://www.dotabuff.com/heroes/' + heroLookup + '/counters?date=' + dates[date - 1]
    headers = {
        'User-Agent':'Mozilla/5.0'
    }
    page = requests.get(URL,headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    #grab sections
    content = soup.find_all('section', class_='counter-outline')

    td_arr = []

    #keep track of which pass this is
    #1 = disadvantages
    #2 = advantages
    x = 1

    #data will comprise of a mainHero and two arrays of heroes they counter/countered by
    data = {"hero":hero,
            "counters":[],
            "countered":[]}

    #for each section
    for elem in content:
        #HEADERS
        #1st pass: COUNTERED BY
        #2nd pass: COUNTERS

        #HEROES
        #counterhero comprises of a hero that the mainHero counters
        counterHero = {"hero":"",
                        "advantage":"",
                        "winrate":""}

        #counteredHero comprises of a hero that counters the mainHero
        counteredHero = {"hero":"",
                        "disadvantage":"",
                        "winrate":""}

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

            name = td_arr[1]
            percent = td_arr[2]
            winrate = td_arr[3]

            #x == 1 --> tracking countered by
            if x == 1:
                counteredHero = {"hero":name,
                    "disadvantage":percent,
                    "winrate":winrate}
                data['countered'].append(counteredHero)
            else:
                counterHero = {"hero":name,
                    "advantage":percent,
                    "winrate":winrate}
                data['counters'].append(counterHero)

            td_arr.clear()

        x += 1
    
    data = json.dumps(data)
    return data