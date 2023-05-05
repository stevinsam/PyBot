# Import required libraries
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import re

# Define a function to get the time and date information
def get_time_and_date(loc):
    try:
        # Check if the input string has 'at' or 'in'
        if re.search(r"\sat\s|\sin\s", loc):
            # Split the string input into location and query
            res = re.split(r"\sat\s|\sin\s", loc)
            # Create a geolocator object
            geolocator = Nominatim(user_agent="PyBotTimezone")
            # Get the geolocation for the given location
            geo = geolocator.geocode(res[1])
            # Get the timezone for the location
            tmzone = TimezoneFinder().timezone_at(lat=geo.latitude,lng=geo.longitude)
            # Get the current date and time for the timezone
            tmzone_now = datetime.now(pytz.timezone(tmzone))
            # Store the formatted date and time
            tmzone_dtime = tmzone_now.strftime("%d/%m/%Y %H:%M:%S")
            # Return the date and time for the location
            return str(f"Current date and time in  {res[1].upper()} is: {tmzone_dtime}")
        else: 
            # Get the current date and time if no location is provided
            now = datetime.now()
            # Store the formatted date and time
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
             # Return the date and time 
            return str(f"The current date and time is {date_time}.")
    except AttributeError:   
        # Return an error message if an invalid location is provided
        return str("Sorry, please enter a valid location")
