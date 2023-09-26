import requests 
import json 
import time
from datetime import datetime 
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
            print("API Response:", api_response) 
            return api_response
        else: 
            print("failed to retrieve API response.")

output = retrieve_request()
def find_count():
# Access the value associated with the key "current count"
    current_count_value = output.get("dedicated_space").get('current_count')

# Check if the key was found in the dictionary
    if current_count_value is not None:
        print("Value associated with 'current_count':", current_count_value)
        return current_count_value
    else:
        print("Key 'current_count' not found in the dictionary.") 

def wait_for_next_multiple_of_5_minutes():
    current_time = datetime.now()
    next_time = current_time.replace(second=0, microsecond=0)
    while next_time.minute % 5 != 0:
        next_time += timedelta(minutes=1)
        time.sleep((next_time - current_time).total_seconds())


#this is the second option, could work gotta look at it later
def wait_for_next_multiple_of_5_minutes():
    global output  # Define output as a global variable
    current_time = datetime.now()
    next_time = current_time.replace(second=0, microsecond=0)
    while next_time.minute % 5 != 0:
        next_time += timedelta(minutes=1)
    time.sleep((next_time - current_time).total_seconds())
    output = retrieve_request()  # Make the API request and assign the result to the global output variable
    find_count()  # Process the API response with find_count


print(find_count())
print(wait_for_next_multiple_of_5_minutes())
