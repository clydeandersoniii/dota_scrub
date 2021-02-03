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
    URL = 'https://www.dotabuff.com/heroes/' + heroLookup.lower() + '/counters?date=' + dates[date - 1]
    print(URL)
    headers = {
        'User-Agent':'Mozilla/5.0'
    }
    page = requests.get(URL,headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    #grab sections
    table = soup.find('table', class_='sortable')
    tbody = table.find('tbody')
    rowArray = tbody.find_all('tr')

    #keep track of which pass this is
    #1 = disadvantages
    #2 = advantages
    x = 1

    #data will comprise of a mainHero and two arrays of heroes they counter/countered by
    data = {"hero":hero,
            "counters":[],
            "countered":[]}

    #for each section
    for row in rowArray:
        #HEROES
        #counterhero comprises of a hero that the mainHero counters
        counterHero = {"hero":"",
                        "advantage":"",
                        "winrate":""}

        #counteredHero comprises of a hero that counters the mainHero
        counteredHero = {"hero":"",
                        "disadvantage":"",
                        "winrate":""}

        tdArray = row.find_all('td')

        hero = tdArray[1].text
        strVantage = tdArray[2].text
        pctVantage = strVantage.replace('%','')
       
        winrate = tdArray[3].text
        pctWinrate = winrate.replace('%','')

        if (float(pctVantage) < 0):
            data['countered'].append({"hero":hero,
                        "disadvantage":pctVantage,
                        "winrate":pctWinrate})  
        else:
            data['counters'].append({"hero":hero,
                        "advantage":pctVantage,
                        "winrate":pctWinrate})

    data = json.dumps(data)
    return data