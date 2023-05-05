from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import re

# Define a function to get the time and date information
def get_time_and_date(loc):
    try:
        if re.search(r"\sat\s|\sin\s", loc):
            res = re.split(r"\sat\s|\sin\s", loc)
            geolocator = Nominatim(user_agent="PyBotTimezone")
            geo = geolocator.geocode(res[1])
            # Get the timezone for the location
            tmzone = TimezoneFinder().timezone_at(lat=geo.latitude,lng=geo.longitude)
            # Get the current date and time for the location
            tmzone_now = datetime.now(pytz.timezone(tmzone))
            tmzone_dtime = tmzone_now.strftime("%d/%m/%Y %H:%M:%S")
            return str(f"Current date and time in  {res[1].upper()} is: {tmzone_dtime}")
        else: 
            now = datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            return str(f"The current date and time is {date_time}.")
    except AttributeError:   
            # showing the error message
            return str("Sorry, please enter a valid location")