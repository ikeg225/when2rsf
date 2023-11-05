import requests 
import time
from datetime import datetime, timedelta
from weather import get_current
from cockroachdb import CockroachDB

cockroach = CockroachDB()

def send_api_request(): 
    url = "https://api.density.io/v2/displays/dsp_956223069054042646" 

    headers = {
        "Authorization" : "Bearer shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e", 
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers) 

    if response.status_code == 200: 
        response_json = response.json() 
        return response_json 
    else:
        print ("API request failed with status code:", response.status_code)
        return None

def retrieve_request():
    if __name__ == '__main__':
        api_response = send_api_request() 
        if api_response: 
            return api_response
        else: 
            print("failed to retrieve API response.")

def find_count(request):
# Access the value associated with the key "current count"
    current_count_value = request.get("dedicated_space").get('current_count')

# Check if the key was found in the dictionary
    if current_count_value is not None:
        return current_count_value
    else:
        print("Key 'current_count' not found in the dictionary.") 

def round_to_nearest_5_minutes(dt):
    minute = dt.minute
    if minute % 5 < 2.5:
        # Round down to the nearest 5 minutes
        dt -= timedelta(minutes=minute % 5)
    else:
        # Round up to the nearest 5 minutes
        dt += timedelta(minutes=5 - minute % 5)
    return dt.replace(second=0, microsecond=0)

def update_every_5_min():
    while True:
        # Get the current time
        now = datetime.now()
        #print(now)

        # Calculate the next multiple of 5 minutes that is also at the first minute of the hour
        next_time = now + timedelta(minutes=5 - now.minute % 5, seconds=-now.second, microseconds=-now.microsecond)
        #print(next_time)

        # Wait until the next multiple of 5 minutes that is also at the first minute of the hour
        time.sleep((next_time - now).total_seconds())

        #Get weather data and current capacity 

        next_time += timedelta(minutes=1)
        weather_data = get_current() 

        curr_time = round_to_nearest_5_minutes(datetime.now())
        current_capacity = find_count(retrieve_request())  
        day_of_week = weather_data.get('day_of_the_week')
        temperature = weather_data.get('temperature')
        temp_feel = weather_data.get('temp_feel')
        weather_code = weather_data.get('weather_code')
        wind_mph = weather_data.get('wind_mph') 
        wind_degree = weather_data.get('wind_degree') 
        pressure_mb = weather_data.get('pressure_mb') 
        precipitation_mm = weather_data.get('precipitation_mm') 
        humidity = weather_data.get('humidity') 
        cloudiness = weather_data.get('cloudiness')
        uv_index = weather_data.get('uv_index')
        gust_mph = weather_data.get('gust_mph')

        #print(weather_data.values())
        
        #Insert data into cockroach database 

        special_days = cockroach.special_day(curr_time)

        cockroach.insert_only_crowdometer_data(
            curr_time, current_capacity, day_of_week, temperature, temp_feel, weather_code, wind_mph,
            wind_degree, pressure_mb, precipitation_mm, humidity, cloudiness, uv_index, gust_mph,
            'school_break' in special_days, 'is_holiday' in special_days, 'is_rrr_week' in special_days,
            'is_finals_week' in special_days, 'is_student_event' in special_days
        )

while True:
    update_every_5_min()