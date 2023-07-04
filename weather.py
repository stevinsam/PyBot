# Import required libraries
from config import OWM_API
import re
from geopy.geocoders import Nominatim
import requests
import json
import spacy
from datetime import datetime

# Store the OpenWeatherMap API key (from the config file)
owm_api_key = OWM_API

# Load the spaCy English model
nlp = spacy.load('en_core_web_sm')


def get_weather_desc(weather_data, location):
    try:
        temp = weather_data['temp']['day']
        humidity = weather_data['humidity']
        wind_speed = weather_data['wind_speed']
        weather_description = weather_data['weather'][0]['description']
        forecast_time = datetime.fromtimestamp(weather_data['dt']).strftime('%A, %d %B %Y')
        return f"""{location.upper():-^20}<br />
            {forecast_time}:<br />
            Temperature: {temp}\N{DEGREE SIGN}C<br />
            Humidity: {humidity}%<br />
            Wind Speed: {wind_speed}mph<br />
            Weather Report: {weather_description}<br /><br />"""
    except KeyError:
        # If any of the required fields are missing, return an error message
        return "Sorry, there was an error processing the weather data.<br />"


def get_location_and_forecast(doc):
    location = None
    forecast = None
    forecast_options = ['today', 'tomorrow', 'weekday', 'weekend']

    for locfrc in doc:
        if locfrc.ent_type_ == 'GPE':
            location = locfrc.text
        elif locfrc.text.lower() in forecast_options:
            forecast = locfrc.text.lower()

    if location is None:
        location = 'London'
    if forecast is None:
        forecast = 'today'

    return location, forecast

# Create a dictionary to store the weather data for each weekday and weekend

# Define a function to get the weekday name from a date string
def get_weekday_name(date_str):
    # Convert the date string to a datetime object
    uxtmsp = datetime.fromtimestamp(date_str)
    dtfmt = uxtmsp.strftime('%Y-%m-%d %H:%M:%S')
    dt = datetime.strptime(dtfmt, '%Y-%m-%d %H:%M:%S')
    # Get the weekday name from the datetime object
    return dt.strftime('%A')

# Define a function called get_weather that takes a location as a parameter
def get_weather(loc):
    try:
        doc = nlp(loc.lower())
        print(loc)
        print(doc)
        print(doc.ents)
        location, forecast = get_location_and_forecast(doc)
        # Use the Nominatim geocoding module to get the latitude and longitude for the city
        geolocator = Nominatim(user_agent="PyBot")
        geo = geolocator.geocode(location)
        # Construct the OpenWeatherMap API endpoint URL with the latitude, longitude, and API key
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={geo.latitude}&lon={geo.longitude}&appid={owm_api_key}&units=metric"
        # Send a GET request to the API endpoint
        response = requests.get(url)
        # Parse the JSON data from the API response
        data = json.loads(response.text)
        weather_list = data['daily']
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            if forecast == 'today':
                return get_weather_desc(weather_list[0], location)
            elif forecast == 'tomorrow':
                    return get_weather_desc(weather_list[1], location)
            elif forecast == 'weekday' or forecast == 'weekend':
                week_data = {
                    "Monday": [],
                    "Tuesday": [],
                    "Wednesday": [],
                    "Thursday": [],
                    "Friday": [],
                    "Saturday": [],
                    "Sunday": []
                }

                # Loop through each forecast item and add it to the appropriate weekday or weekend list
                for item in weather_list:
                    weekday_name = get_weekday_name(item["dt"])

                    
                    # Add the forecast item to the appropriate weekday or weekend list
                    if weekday_name in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                                week_data[weekday_name].append(item)
                
                                                           
                    # Check if all dictionary items have only one item, and stop the loop if they do
                    if all(len(items) == 1 for items in week_data.values()):
                        break
                    
                    
        
                # Get weather for weekdays or weekends
                weather_str = ""
                if forecast == 'weekday':
                    for weekday, weather_items in week_data.items():
                        if weekday not in ['Saturday', 'Sunday'] and len(weather_items) > 0:
                            print(weekday.upper())
                            weather_str += f"{weekday.upper()}</br>"
                            for weather_item in weather_items:
                                weather_str += get_weather_desc(weather_item, location) + "</br>"
                elif forecast == 'weekend':
                    for weekday, weather_items in week_data.items():
                        if weekday in ['Saturday', 'Sunday'] and len(weather_items) > 0:
                            print(weekday.upper())
                            weather_str += f"{weekday.upper()}</br>"
                            for weather_item in weather_items:
                                weather_str += get_weather_desc(weather_item, location) + "</br>"
                
                if len(weather_str) > 0:
                    return weather_str.strip()
        else:
            return str("Sorry connection issue with OWM API")
    except AttributeError:   
            # If the location is invalid, return an error message
            return str("Sorry, please enter a valid location")