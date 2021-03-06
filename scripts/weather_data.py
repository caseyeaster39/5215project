import requests
import json

from meteostat import Point, Hourly
from datetime import timedelta


def get_user_key():
    try:
        with open('.key_cache/weather_key.txt', 'r') as fin:
            key = fin.read()
    except FileNotFoundError:
        print('User key not found. You can create an account here: https://home.openweathermap.org/')
        key = input('Please paste your key here: ')
        with open('.key_cache/weather_key.txt', 'w') as fout:
            fout.write(key)
    return key


def weather_req_now(latlong):
    lat = latlong[0]
    lon = latlong[1]
    key = get_user_key()

    request_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}'

    resp = requests.get(request_url)
    resp.raise_for_status()

    resp = json.dumps(resp.json())
    resp = process_weather_response(resp)
    return resp


def process_weather_response(resp):
    resp = json.loads(resp)
    output = {
        'main': resp['weather'][0]['main'],
        'temp_faren': (resp['main']['temp'] - 273.15) * 9/5 + 32,
        'visibility': resp['visibility'],
        'wind_speed': resp['wind']['speed'],
        'clouds': resp['clouds']['all']
    }
    return output


def search_weather(lat, lon, start):
    end = start + timedelta(days=1)

    location = Point(lat, lon, 70)

    hour_df = Hourly(location, start, end)
    hour_df = hour_df.fetch()
    return hour_df
