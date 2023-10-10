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

    #WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    WEATHER_API_KEY = "deb0a1d4b83849728e4215914230610"
    day = "2022-10-12"
    parameters = {
        'q': 'berkeley',
        'dt': day,
    }

    response = requests.get(f'http://api.weatherapi.com/v1/history.json?key={WEATHER_API_KEY}', params = parameters)
    if response.status_code == 200:

        data = response.json()
        hourly_data = data["forecast"]["forecastday"][0]["hour"]
        date_object = datetime.strptime(day, "%Y-%m-%d")
        day_of_week = date_object.isoweekday()
        hourly_dict = {}
        for hour in hourly_data:
            time = hour['time']
            temperature = hour['temp_c']
            temp_feel = hour['feelslike_c']
            weather_code = hour['condition']['code']
            wind_mph = hour['wind_mph']
            wind_degree = hour['wind_degree']
            pressure_mb = hour['pressure_mb']
            precipitation_mm = hour['precip_mm']
            humidity = hour['humidity']
            cloudiness = hour['cloud']
            uv_index = hour['uv']
            gust_mph = hour['gust_mph']

            hourly_dict[time] = {
                'day_of_week': day_of_week+1,  
                'temperature': temperature,
                'temp_feel': temp_feel,
                'weather_code': weather_code,
                'wind_mph': wind_mph,
                'wind_degree': wind_degree,
                'pressure_mb': pressure_mb,
                'precipitation_mm': precipitation_mm,
                'humidity': humidity,
                'cloudiness': cloudiness,
                'uv_index': uv_index,
                'gust_mph': gust_mph,
            }  
    else:
        # Handle the error
        print(f"Error: API request failed with status code {response.status_code}")

        
    return hourly_dict


print(get_history("2022-10-10 07:20:00"))



