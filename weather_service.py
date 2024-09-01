import requests
from geopy.geocoders import Nominatim
from ipinfo import getHandler

API_KEY = '503ef210442da7c03a42423978255b4e'  
BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'

def get_weather_by_city(city_name):
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return None

def get_weather_by_coordinates(latitude, longitude):
    params = {
        'lat': latitude,
        'lon': longitude,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return None

def get_current_location(ipinfo_token):
    try:
        handler = getHandler(ipinfo_token)
        details = handler.getDetails()
        
        latitude = details.latitude
        longitude = details.longitude
        
        return latitude, longitude
    except Exception as e:
        print(f"Error getting location: {e}")
        return None, None