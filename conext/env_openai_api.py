import openai
import requests
import json
import re
import os
import time
import RPi.GPIO as GPIO

# VARIABLES that can be adjusted
CONTEXT_FILE = 'context_file.txt' # file that provides training data
RAW_DATA_FILE = 'raw_data.txt' # file that provides raw data
OUTPUT_FILE = 'output.txt' #file that writes gpt response (overwrite)

# openAI api request
def httpRequest(prompt):
    

    api_key = os.getenv("OPENAI_API_KEY")

    url = 'https://api.openai.com/v1/chat/completions'
    

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=prompt).json()
    print(response)

    try:
        print("\nResponse:")
        generated_text = response["choices"][0]["message"]["content"]
        print(generated_text)
        return generated_text
    except:
        print(f"Request failed with status code {response['error']}")


def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(15, GPIO.OUT)
    GPIO.output(15, GPIO.LOW)
    
    # TODO
    messages = [{"role":"system","content":"You are an Assistant."}]
    # Load prompt file
    
    with open(CONTEXT_FILE, 'r') as f:
        context = f.read()
        # print("length of prompt!", len(context))  # length is like 9thousand
        messages.append({"role": "user", "content": "{}".format(context)})

    # perform api call num_of_times times
    num_of_times = 1
    for i in range(num_of_times):

        # Load raw data file
        filename3 = RAW_DATA_FILE        
        prompt_msg = ""

        with open(filename3, 'r') as f:
            prompt_msg += f.read()
        
        messages.append({"role": "user", "content": "{}".format(prompt_msg)})
        
        prompt = {
            "messages":messages,
            "model": "gpt-4",
            "temperature":0
        }
        print("Prompt {} has been sent. Waiting for response...".format(i+1))
        start_time = time.time()
        apiResponse = httpRequest(prompt)
        end_time = time.time()
        print(end_time-start_time,"s has elapsed")
        # print(apiResponse)
        with open(OUTPUT_FILE, 'w') as o:
            o.write(apiResponse)
        
        messages.pop()

    # end_time = time.time()
    GPIO.output(15, GPIO.HIGH)
    # print(end_time-start_time,"s has elapsed")
    with open(OUTPUT_FILE, 'a') as o:
            o.write(str(end_time))

    GPIO.cleanup()
main()
