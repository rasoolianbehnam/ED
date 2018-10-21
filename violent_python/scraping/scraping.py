import requests
from bs4 import BeautifulSoup
import time
import re

def weather_forecast():
    page = requests.get('https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168')
    soup = BeautifulSoup(page.content, 'html.parser')

    seven_day = soup.find(id='seven-day-forecast-container')
    forecast_items = seven_day.find_all(class_='forecast-tombstone')

    for day in forecast_items:
        time = day.find(class_='period-name').get_text()
        short_desc = day.find(class_='short-desc').get_text()
        temp = day.find(class_='temp').get_text()
        #print(time)
        print(time)
        print(short_desc)
        print(temp)
        print('*************************')

def imdb_dvd(file_name='result.md'):
    page = requests.get('https://www.imdb.com/list/ls016522954/?ref_=nv_tvv_dvd')
    soup = BeautifulSoup(page.content, 'html.parser')
    
    items = soup.find_all(class_='lister-item-content')
    print('|Title|Type|Year|rating|')
    print('|-----|----|----|------|')
    for item in items:
        movie_name = item.find('a').get_text()
        year = item.find(class_='lister-item-year').get_text()
        ranking = item.find(class_='ipl-rating-star__rating')
        movies = re.findall('\(\\d\\d\\d\\d\)', year, re.M|re.I)
        series = re.findall('\\d\\d\\d\\d', year, re.M|re.I)
        if len(movies) > 0:
            title = 'Movie'
            year = movies[0]
        elif len(series) == 1:
            title = 'Series (in progress)'
            year = series[0]
        elif len(series) == 2:
            title = 'Series (finished)'
            year = '%s - %s' %(series[0], series[1])
        line = "|%s|%s|%s|%s|"%(movie_name, title, year, ranking.text)
        line = line.encode('utf8')
        print(line)

def wells():
    url = 'https://connect.secure.wellsfargo.com/auth/login/do'

    data = {'destination':'AccountSummary',
            'hdnuserid':''
            ,'homepage':'true',
            'j_password':'cD2D9c27',
            'j_username':'bzr0014',
            'jsenabled':'true',
            'origin':'cob',
            'origination':'WebCons',
            'save-username':'false',
            'screenid':'SIGNON'}
    r = requests.post(url, data=data)
    print(r.content)


def rec():
    page = requests.get('http://www.calendarwiz.com/calendars/week.php?crd=aurec&cid[]=all&PHPSESSID=e4ebeddb5164381c8ae8bd4fc3a656f1&jsenabled=1&winh=670&winw=1301&inifr=false')
    #print(page.content)
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.find_all('td')
    for row in rows:
        hour_open = row.find(class_='cat136656')
        hour_closed = row.find(class_='cat231547')
        day = row.find('b')
        if day is not None:
            print(day.text)
        if hour_open is not None:
            print(hour_open.text)
        if hour_closed is not None:
            print(hour_closed.text)
    #for hour in hours:
    #    print hour
 
#imdb_dvd()
#rec()
imdb_dvd()
