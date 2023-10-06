from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

def get_current():
    load_dotenv()

    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

    parameters = {
        'q': 'berkeley',
        'days': 3,
        'exclude': 'current,minutely,hourly,astronomy'
    }


    response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}', params = parameters)

    #print(response.text)
    if response.status_code == 200:
        # The request was successful (HTTP 200 OK).
        
        # Parse the JSON response
        data = response.json()
        # Put data into dictionary
        data_dict = {
            'time' : data['location']['localtime'],
            'day_of_the_week' : data['current']['is_day'] + 1,
            'temperature' : data['current']['temp_f'],
            #'description' : data['current']['condition']['text'],
            'temp_feel' : data['current']['feelslike_f'],
            'weather_code' : data['current']['condition']['code'],
            'wind_mph' : data['current']['wind_mph'],
            'wind_degree' : data['current']['wind_degree'],
            'pressure_mb' : data['current']['pressure_mb'],
            'precipitation_mm' : data['current']['precip_mm'],
            'humidity' : data['current']['humidity'],
            'cloudiness' : data['current']['cloud'],
            'uv_index' : data['current']['uv'],
            'gust_mph' : data['current']['gust_mph'],
        }

        # Access and use the data
        temperature = data['current']['temp_f']
        description = data['current']['condition']['text']
        day_of_the_week = data['current']['is_day'] + 1
        temp_feel = data['current']['feelslike_f']
       # weather_code = data['current']['code']
        # Get today's date and calculate the date for the next day
        today = datetime.now().date()
        next_day = today + timedelta(days=1)

        # Find the forecast for the next day
        '''for forecast in data['forecast']['forecastday']:
            date = datetime.strptime(forecast['date'], '%Y-%m-%d').date()
            if date == next_day:
                next_day_forecast = forecast
                break
        '''
        #chance_of_rain = tomorrow_forecast['day']['daily_chance_of_rain']
        # Print the weather information
        '''   print("Date:", today)
        print(f"Day of the Week: {day_of_the_week}")
        print(f"Temperature: {temperature}°F")
        print(f"Feels Like: ", temp_feel, "°F")
        print(f"Weather Code: ", weather_code)
        print(f"Description: {description}")
        print()
        # Print forcast for next day
        print("Forecast for the next day:")
        print(f"Date: {next_day_forecast['date']}")
    #  print(f"Day of the Week: {next_day_forecast['is_day']}")
        print(f"Temperature: {next_day_forecast['day']['avgtemp_f']}°F")
        #print(f"Description: {next_day_forecast['day']['condition']['text']}") this prints text, not a percentage of probability it will rain
        print(f"Description: {next_day_forecast['day']['daily_chance_of_rain']}") #this just adds all the percentages together
        print("other alg")
        '''
        '''
        tomorrow = today + timedelta(days=1)
        for forecast in data['forecast']['forecastday']:
            date = datetime.strptime(forecast['date'], '%Y-%m-%d').date()
            if date == tomorrow:
                tomorrow_forecast = forecast
                break
            
        # Extract the chance of rain for tomorrow
        chance_of_rain = tomorrow_forecast['day']['daily_chance_of_rain']

        # Display the chance of rain for tomorrow
        print(f"Chance of rain for tomorrow: {chance_of_rain}%") #think this just adds up the total percentages.
        '''

    else:
        # Handle the error
        print(f"Error: API request failed with status code {response.status_code}")

    return data_dict

#print(get_current())

'''def get_dict():
    return data_dict'''


def get_history(date):

    str_date = str(date).split()

    day = str_date[0] # example: 2022-10-01
    time = str_date[1] # example: 07:20:00

    load_dotenv()

    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

    parameters = {
        'q': 'berkeley',
        'dt': day,
    }

    response = requests.get(f'http://api.weatherapi.com/v1/history.json?key={WEATHER_API_KEY}', params = parameters)

    hourly_forecast = response["forecast"]["forecastday"][0]["hour"]

    for hour in hourly_forecast:
        time = hour["time"]
        temperature_c = hour["temp_c"]
        condition = hour["condition"]["text"]
        print(f"Time: {time}, Temperature: {temperature_c}°C, Condition: {condition}")

    return response.text


print(get_history("2022-10-03 07:20:00"))



