import requests 
import json 
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

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
            print("API Response:", "Works") 
            return api_response
        else: 
            print("failed to retrieve API response.")

output = retrieve_request()
def find_count(request):
# Access the value associated with the key "current count"
    current_count_value = request.get("dedicated_space").get('current_count')

# Check if the key was found in the dictionary
    if current_count_value is not None:
        print("Value associated with 'current_count':", current_count_value)
        return current_count_value
    else:
        print("Key 'current_count' not found in the dictionary.") 


def wait_for_next_multiple_of_5_minutes():
    while True:
        # Get the current time
        now = datetime.now()
        print(now)

        # Calculate the next multiple of 5 minutes that is also at the first minute of the hour
        next_time = now + timedelta(minutes=5 - now.minute % 5, seconds=-now.second, microseconds=-now.microsecond)
        print(next_time)

        # Wait until the next multiple of 5 minutes that is also at the first minute of the hour
        time.sleep((next_time - now).total_seconds())

        # Call find_count() and return the output
        next_time += timedelta(minutes=1)
        data = retrieve_request()
        print(find_count(data))

#print(find_count(retrieve_request()))
wait_for_next_multiple_of_5_minutes()
