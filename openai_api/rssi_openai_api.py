import openai
import requests
import json
import re
import os
import time
import tiktoken

# VARIABLES that can be adjusted
CONTEXT_FILE = 'data/rssi_context_file.txt' # file that provides training data
RAW_DATA_FILE = 'data/rssi_raw_data.txt' # file that provides raw data
OUTPUT_FILE = '../http_request/data/rssi_output.txt' # output file from gpt

# openAI api request
def httpRequest(prompt):
    

    api_key = os.getenv("OPENAI_API_KEY")

    url = 'https://api.openai.com/v1/chat/completions'
    

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=prompt).json()

    try:
        print("\nResponse:")
        generated_text = response["choices"][0]["message"]["content"]
        print(generated_text)
        return generated_text
    except:
        print(f"Request failed with status code {response['error']}")


def main():
    start_time = time.time()
    # TODO
    messages = [{"role":"system","content":"I want you to act as an data scientist. \
                 Given some data sets of locations, analyse the pattern to give the location of an unknown data set"}]
    # Load prompt file
    
    with open(CONTEXT_FILE, 'r') as f:
        context = f.read()
        # print("length of prompt!", len(context))  # length is like 9thousand
        messages.append({"role": "user", "content": "{}".format(context)})

    
    while True:

        # Waiting for prompt
        # TODO
        filename = RAW_DATA_FILE
        last_modified_time = os.path.getmtime(filename)
        print("Waiting for prompt...")
        while True:
            current_modified_time = os.path.getmtime(filename)
            if current_modified_time != last_modified_time:
                # print("File has been updated!")
                last_modified_time = current_modified_time
                break
            time.sleep(1)  # wait for 1 second before checking again
    

        # perform api call num_of_times times
        num_of_times = 1
        for i in range(num_of_times):

            # Load raw data file
            filename3 = RAW_DATA_FILE        
            prompt_msg = "Unknown:\n"

            with open(filename3, 'r') as f:
                prompt_msg += f.read()

            # prompt_msg +="\n\nAnswer:"
            
            messages.append({"role": "user", "content": "{}".format(prompt_msg)})
            

            # encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            # num_tokens = len(encoding.encode(str(messages)))
            # print("num tokens: ", num_tokens)

            # edit here
            prompt = {
                "messages":messages,
                "model": "gpt-4",
                "temperature":0.3
            }

            print("Prompt {} has been sent. Waiting for response...".format(i+1))
            apiResponse = httpRequest(prompt)
            with open(OUTPUT_FILE, 'w') as o:
                o.write(apiResponse)
            messages.pop()

        end_time = time.time()
        # print(end_time-start_time,"s has elapsed")

main()
