import serial
import numpy as np
from scipy.io.wavfile import write
from dotenv import load_dotenv
import os
import openai
import time
import keyboard
import uuid
import requests
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import requests

# Config variables
goal_url = "http://192.168.133.100/api/NaviBee/robottask"
LOCAL_LLM_IP = "192.168.133.235"

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = os.getenv("OPENAI_API_KEY")

########## Sending speech data to serial from Arduino and Receiving from laptop ########## 

#press r to start recording
SAMPLE_RATE = 4000  # Must match the Arduino's sample rate

# Set up serial connection (modify the COM port accordingly)
ser = serial.Serial('COM5', 250000)
data = []

print("Press 'r' to start recording...")

# Wait until 'r' is pressed to start recording
keyboard.wait('r')

print("Recording... Press 'r' again to stop.")
time.sleep(0.5)  # Introduce a small delay

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        value = int(line)
        data.append(value)
    except:
        pass
    
    # Check if 'r' is pressed to stop recording
    if keyboard.is_pressed('r'):
        break

print("Saving...")
data = np.array(data, dtype=np.int16)
write("output.wav", SAMPLE_RATE, data)
ser.close()

time.sleep(5)

########## Transcribing speech to text, then sending to local model for analysis ##########
audio_file = open("output.wav", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
print(transcript)



def get_location(speech_data):
    response = requests.post(LOCAL_LLM_IP, data=speech_data)
    return response

########## Sending instructions to robot ##########

# Define the locations
# locations = ['Meeting Room', 'Entrance', 'C', 'D', 'E', 'Table']
locations = ['Meeting Room', 'Entrance', 'Table']

data = {}  # Dictionary to hold the content of the JSON files for each location

# Loop over each location to open and read the JSON files

for location in locations:
    with open(f'locations_data/location_{location}.json', 'r') as file:
        data[location] = json.load(file)
    
    # Update the 'jobid' with a new UUID
    data[location]['jobid'] = str(uuid.uuid4())

next_location = get_location(transcript['text'])
response = requests.post(goal_url, json= data[next_location])

post_response_json = response.json()
print(next_location)
print(response.status_code)
print(post_response_json)