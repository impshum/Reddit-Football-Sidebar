from requests import get
import json


football_api_key = 'XXXX'


def get_json(url):
    r = get(f'{url}&APIkey={football_api_key}')
    if r.status_code == 200:
        return r.json()


def get_countries():
    data = get_json(f'https://apiv2.apifootball.com/?action=get_countries')
    print(data)


def get_leagues(country_id):
    data = get_json(f'https://apiv2.apifootball.com/?action=get_leagues&country_id={country_id}')
    print(data)


def get_league_standings(league_id):
    data = get_json(f'https://apiv2.apifootball.com/?action=get_standings&league_id={league_id}')
    print(data)


def get_fixtures(date_from, date_to, league_id):
    data = get_json(f'https://apiv2.apifootball.com/?action=get_events&from={date_from}&to={date_to}&league_id={league_id}')
    print(data)


#get_countries()
#get_leagues(46)
#get_league_standings(149)
#get_fixtures('2020-10-15', '2020-10-30', 149)
