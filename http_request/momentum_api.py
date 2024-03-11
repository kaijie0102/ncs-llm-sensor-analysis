import requests
import json

def send_post_request(api_endpoint, data_payload):
    headers = {
        'Content-Type': 'application/json',
        # Include any other necessary headers here.
    }
    
    response = requests.post(api_endpoint, data=json.dumps(data_payload), headers=headers)
    
    return response

if __name__ == '__main__':
    estimated_location = "Server Rack"

    API_ENDPOINT = 'http://192.168.112.135:5000'  # Replace with your API endpoint.
    DATA_PAYLOAD = {
        'location': estimated_location,
        # Add other data as needed.
    }
    HEADER = {
            'Content-Type': 'applications/json'
            }
    
    response = send_post_request(API_ENDPOINT, DATA_PAYLOAD)
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")

