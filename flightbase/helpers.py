import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid
import json

from flask import redirect, render_template, session
from functools import wraps

def error(message):
    """Render message as an error to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", msg=escape(message))


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def weather_lookup(weather_api, lat, lng):
    """Lookup city weather"""
    api_base = 'https://api.openweathermap.org/data/2.5/weather'

    try: 
        weather_params = {
            'lat': lat,
            'lon': lng,
            'appid': weather_api,
            'units': 'metric'
        }

        weather_result = requests.get(api_base, weather_params)
        weather_response = weather_result.json()
        return weather_response

    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None

def airport_lookup(flight_api, airport):
    """Lookup airport details"""
    api_base = 'http://airlabs.co/api/v9/'

    try: 
        airport_params = {
            'api_key': flight_api,
            'iata_code': airport
            }
        airport_result = requests.get(api_base+'airports', airport_params)
        airport_response = airport_result.json()
        return airport_response

    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None


def flight_lookup(flight_api, weather_api, flight):
    """Lookup flight details"""

    api_base = 'http://airlabs.co/api/v9/'

    # Flight lookup
    try: 
        flight_params = {
            'api_key': flight_api,
            'flight_iata': flight
            }
        flight_result = requests.get(api_base+'flight', flight_params)
        flight_response = flight_result.json()
    
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None

    if 'response' in flight_response:
        flight_dict = flight_response['response']
        
        # Airport lookup
        orig_dict = airport_lookup(flight_api, flight_dict['dep_iata'])['response'][0]
        dest_dict = airport_lookup(flight_api, flight_dict['arr_iata'])['response'][0]

        # Weather lookup
        orig_temp = weather_lookup(weather_api, orig_dict['lat'], orig_dict['lng'])['main']
        dest_temp = weather_lookup(weather_api, dest_dict['lat'], dest_dict['lng'])['main']
        orig_weather = weather_lookup(weather_api, orig_dict['lat'], orig_dict['lng'])['weather'][0]
        dest_weather = weather_lookup(weather_api, dest_dict['lat'], dest_dict['lng'])['weather'][0]

        total = float(flight_dict['arr_time_ts']) - float(flight_dict['dep_time_ts'])
        current = float(flight_dict['updated']) - float(flight_dict['dep_time_ts'])
        flight_progress = (current / total) * 100

        if flight_progress > 100:
            flight_progress = 100
        elif flight_progress < 0:
            flight_progress = 0

        return {
            "flight_number": flight_dict['flight_iata'],
            "flight_logo": flight_dict['airline_iata'],
            "airline_name": flight_dict['airline_name'],
            "dep_time": flight_dict['dep_time'],
            "arr_time": flight_dict['arr_time'],
            "progress": flight_progress,
            "dep_iata": flight_dict['dep_iata'],
            "arr_iata": flight_dict['arr_iata'],
            "dep_city": flight_dict['dep_city'],
            "arr_city": flight_dict['arr_city'],
            "dep_name": flight_dict['dep_name'],
            "arr_name": flight_dict['arr_name'],
            "status": flight_dict['status'],
            "dep_code": orig_dict['country_code'],
            "arr_code": dest_dict['country_code'],
            "dep_flag": orig_dict['country_code'].lower(),
            "arr_flag": dest_dict['country_code'].lower(),
            "dep_temp": orig_temp['temp'],
            "arr_temp": dest_temp['temp'],
            "dep_tempMin": orig_temp['temp_min'],
            "arr_tempMin": dest_temp['temp_min'],
            "dep_tempMax": orig_temp['temp_max'],
            "arr_tempMax": dest_temp['temp_max'],
            "dep_weather": orig_weather['main'],
            "arr_weather": dest_weather['main'],
            "dep_weatherIcon": orig_weather['icon'],
            "arr_weatherIcon": dest_weather['icon']
        }
    else:
        return flight_response['error']
    


    