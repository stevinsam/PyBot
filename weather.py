# Import required libraries
from config import OWM_API
import re
from geopy.geocoders import Nominatim
import requests
import json

# Store the OpenWeatherMap API key (from the config file)
owm_api_key = OWM_API

# Define a function called get_weather that takes a location as a parameter
def get_weather(loc):
    try:
        # Use regex to split the string to get the location after the 'at' or 'in' input
        res = re.split(r"\sat\s|\sin\s", loc)
        city = res[1]
        # Use the Nominatim geocoding module to get the latitude and longitude for the city
        geolocator = Nominatim(user_agent="PyBot")
        geo = geolocator.geocode(city)
        # Construct the OpenWeatherMap API endpoint URL with the latitude, longitude, and API key
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={geo.latitude}&lon={geo.longitude}&units=metric&appid={owm_api_key}"
        # Send a GET request to the API endpoint
        response = requests.get(url)
        # Parse the JSON data from the API response
        data = json.loads(response.text)
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Extract the current weather data of the chosen location from the API response
            data = response.json()
            current = data['current']
            temperature = (current['temp'])
            humidity = (current['humidity'])
            wind_speed = (round(current['wind_speed'] * 2.23694))
            report = (current['weather'])
            # Return a string containing the weather data for the location
            return str(f"""
            {city.upper():-^20}<br />
            Temperature: {temperature}\N{DEGREE SIGN}C<br />
            Humidity: {humidity}%<br />
            Wind Speed: {wind_speed}mph<br />
            Weather Report: {report[0]['description']}""")
    except AttributeError:   
            # If the location is invalid, return an error message
            return str("Sorry, please enter a valid location")