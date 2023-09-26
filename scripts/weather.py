from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

parameters = {
    'q': 'berkeley',
    'days': 3,
    'exclude': 'current,minutely,hourly,astronomy'
}

response = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}', params = parameters)

#print(response.text)
if response.status_code == 200:
    # The request was successful (HTTP 200 OK).
    
    # Parse the JSON response
    data = response.json()
    
    # Access and use the data
    temperature = data['current']['temp_c']
    description = data['current']['condition']['text']

    # Get today's date and calculate the date for the next day
    today = datetime.now().date()
    next_day = today + timedelta(days=1)

    # Find the forecast for the next day
    for forecast in data['forecast']['forecastday']:
        date = datetime.strptime(forecast['date'], '%Y-%m-%d').date()
        if date == next_day:
            next_day_forecast = forecast
            break
    #chance_of_rain = tomorrow_forecast['day']['daily_chance_of_rain']
    # Print the weather information
    print(f"Temperature: {temperature}°C")
    print(f"Description: {description}")
    # Print forcast for next day
    print("Forecast for the next day:")
    print(f"Date: {next_day_forecast['date']}")
    print(f"Temperature: {next_day_forecast['day']['avgtemp_c']}°C")
    #print(f"Description: {next_day_forecast['day']['condition']['text']}") this prints text, not a percentage of probability it will rain
    print(f"Description: {next_day_forecast['day']['daily_chance_of_rain']}") #this just adds all the percentages together
    print("other alg")
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


else:
    # Handle the error
    print(f"Error: API request failed with status code {response.status_code}")