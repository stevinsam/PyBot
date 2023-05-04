import config
import re
from geopy.geocoders import Nominatim
import requests
import json
# Get the OpenWeatherMap API key
owm_api_key = config.OWM_API

def get_weather(loc):
    try:
        res = re.split(r"\sat\s|\sin\s", loc)
        city = res[1]
        geolocator = Nominatim(user_agent="PyBot")
        geo = geolocator.geocode(city)
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={geo.latitude}&lon={geo.longitude}&units=metric&appid={owm_api_key}"
        response = requests.get(url)
        data = json.loads(response.text)
        if response.status_code == 200:
            data = response.json()
            current = data['current']
            temperature = (current['temp'])
            humidity = (current['humidity'])
            wind_speed = (round(current['wind_speed'] * 2.23694))
            report = (current['weather'])
            return str(f"""
            {city.upper():-^20}<br />
            Temperature: {temperature}\N{DEGREE SIGN}C<br />
            Humidity: {humidity}%<br />
            Wind Speed: {wind_speed}mph<br />
            Weather Report: {report[0]['description']}""")
    except AttributeError:   
            # showing the error message
            return str("Sorry that location does not exist")