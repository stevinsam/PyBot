from datetime import datetime

# Define a function to get the time and date information
def get_time_and_date():
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    return str(f"The current date and time is {date_time}.")