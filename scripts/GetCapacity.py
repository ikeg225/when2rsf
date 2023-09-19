import requests 
import json 

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


print(find_count())

