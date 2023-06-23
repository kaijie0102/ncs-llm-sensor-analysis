import openai
import requests
import json
import re
import os
import time
import tiktoken

# VARIABLES that can be adjusted
TRAINING_FILE = 'before_finetune.txt' # file that provides training data
RAW_DATA_FILE = 'mqtt_message.txt' # file that provides raw data

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
    messages = [{"role":"system","content":"I want you to act as an data scientist. Given a data set, analyse the pattern to give the correct number of taps. Several Data and Answers will be given as example"}]
    # Load prompt file
    
    with open(TRAINING_FILE, 'r') as f:
        prompt1 = f.read()
        # print("length of prompt!", len(prompt1))  # length is like 9thousand
        messages.append({"role": "user", "content": "{}".format(prompt1)})

    
    # while True:

    #     # Waiting for prompt
    #     # TODO
    #     filename = "mqtt_message.txt"
    #     last_modified_time = os.path.getmtime(filename)
    #     print("Waiting for prompt...")
    #     while True:
    #         current_modified_time = os.path.getmtime(filename)
    #         if current_modified_time != last_modified_time:
    #             # print("File has been updated!")
    #             last_modified_time = current_modified_time
    #             break
    #         time.sleep(1)  # wait for 1 second before checking again
    

    # do num_of_times times
    num_of_times = 10
    for i in range(num_of_times):

        # Load raw data file
        filename3 = RAW_DATA_FILE        
        prompt3 = "Data:\n"

        with open(filename3, 'r') as f:
            prompt3 += f.read()

        prompt3 +="\n\nAnswer:"

        # # splitting up long prompt into multiple prompts
        # chunk_size = 512
        # chunks = re.findall('.{1,' + str(chunk_size) + '}(?:\\s+|$)', prompt1)
        
        # for chunk in chunks:
        #     # print(chunk)
        #     pass
        #     #messages.append({"role": "system", "content": "{}".format(chunk)})
        
        messages.append({"role": "user", "content": "{}".format(prompt3)})
        
        # print("here is messages: ",messages)


        # encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        # num_tokens = len(encoding.encode(str(messages)))
        # print("num tokens: ", num_tokens)

        # edit here
        prompt = {
            # "messages": [
            #     {"role": "user", "content": "{}".format(prompt3)}  # ,
            #     # {"role": "user","content":"{}".format(prompt2)}

            # ],
            "messages":messages,
            "model": "gpt-3.5-turbo-16k",
            "temperature":0.3
        }

        # model = "gpt-3.5-turbo"

        # response = openai.ChatCompletion.create(
        #     engine=model,
        #     prompt=prompt,
        #     # temperature=0.5,
        #     # max_tokens=100,
        #     # top_p=1,
        #     # frequency_penalty=0,
        #     # presence_penalty=0
        # )

        # print("Prompt \"{}\" has been sent. Waiting for response...".format(prompt3))
        print("Prompt {} has been sent. Waiting for response...".format(i+1))
        apiResponse = httpRequest(prompt)
        messages.pop()
        # messages.append({"role":"assistant", "content":"{}".format(apiResponse)})

    end_time = time.time()
    print(end_time-start_time,"s has elapsed")
main()
