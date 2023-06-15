import openai
import requests
import os
import time

"""
Variables that requires user inputs will be marked with TODO
"""
# FINETUNED_MODEL = "ada:ft-personal-2023-06-01-09-57-07"
# FINETUNED_MODEL = "ada:ft-personal-2023-06-05-08-24-08"
FINETUNED_MODEL = "ada:ft-personal-2023-06-05-08-58-58"
# openAI api request
def httpRequest(prompt):
    
    url = 'https://api.openai.com/v1/completions'
    api_key = os.getenv("OPENAI_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=prompt).json()
    try:
        # cases
        ONE_TAP  = "one tap"
        TWO_TAPS = "two taps"
        THREE_TAPS = "three taps"

        print("\nResponse:")
        generated_text = response["choices"][0]["text"]
        # print("generated_text: ", generated_text)

        if ONE_TAP in generated_text:
            return 1
        elif TWO_TAPS in generated_text:
            return 2
        elif THREE_TAPS in generated_text:
            return 3
        else:
            return "Unknown"
        # return generated_text
    except:
        print(f"Request failed with status code {response['error']}")


def main():

    # number of times to call api
    num_times = 100
    start_time = time.time()
    for i in range(num_times):
        # Load mqtt file
        filename3 = 'raw_data.txt'
        prompt = "Data:\n"
        with open(filename3, 'r') as f:
            prompt += f.read()
        prompt+="\n\nAnswer:"

        
        # print(prompt)

        # edit here
        prompt = {
            "prompt":prompt,
            # change model when it is updated
            "model": FINETUNED_MODEL,
            "temperature":0.3
        }

        print("Prompt {} has been sent. Waiting for response...".format(i+1))
        apiResponse = httpRequest(prompt)

        print("{} tap(s) detected".format(apiResponse))
    end_time = time.time()
    print(end_time-start_time,"s has elapsed")

main()
