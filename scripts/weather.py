import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

parameters = {
    'q': 'berkeley'
}

response = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}', params = parameters)

print(response.text)