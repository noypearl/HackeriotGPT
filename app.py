import json
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import openai
import os
import random
import string

app = Flask(__name__)

CORS(app) # TODO - fix this when I'm alive!
# gpt = GPT(engine="text-davinci-002", temperature=0.5)
MODEL = "gpt-3.5-turbo" # TODO - check if there's a cheaper mode (?)
messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]
# OPENAPI_KEY= os.environ.get('API_KEY') # TODO - use a hidden env file`
# Store the passwords for each level
# passwords = ["Hackeriot" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) for _ in range(13)]
#passwords_arr = ["H4cerIoT", "hackeriotIsCOOL", "w3Ar3Hack3riot", "breakingCHATHackeriot", "HackForFun","myGPTisBetterThanYours","WhatAmIHacking","lolImHacker","h4ck3ed","GPT-FTW","woohooCyber","CyberHackeriot","HackeriotAI"]
passwords_arr = ["Hackeriot" + str(_) for _ in range(13)]
print(f"passwords: {passwords_arr}")

with open("levels.json", "r") as f:
    levels_json = json.load(f)
system = levels_json['system']

# notice levels are starting from 1 in GUI + REST API!
data = {'passwords_arr': passwords_arr, 'assistant_arr': levels_json['assistant'], 'system_arr': levels_json['system'], 'initial': levels_json['initial']}

# return response according to prompt + level

@app.route('/')
def show_home():
    return render_template("index.html", title = 'HackeriotGPT')


def send_prompt_get_response(level, prompt):
    system_initial_message = data['initial'].replace("$pass", data["passwords_arr"][level-1])
    print(f"Sending prompt, level: {level}, prompt: {prompt}, full system message: {system_initial_message}")
    gpt_messages = [
        {"role": "system", "content": system_initial_message + data['system_arr'][level - 1]},
        {"role": "user", "content": prompt}
    ]
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAPI_KEY}'
    }
    body = {
        'model': MODEL,
        'messages': gpt_messages,
        'temperature': 0.7
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(body))
    response_data = response.json()
    assistant_response = response_data['choices'][0]['message']['content']
    if level + 1 >= len(data['system_arr']):
        return {"success": True, "system": "You finished ALL THE CHALLENGES! OMG SUCH Hackerit!"}
    else:
        next_challenge_system = data['system_arr'][level+1]
        return {"success": True, "response" :assistant_response, "system": next_challenge_system}


# Send level + password and try to get next challenge!
@app.route('/api/checkpass', methods=['POST'])
@cross_origin()
def check_password_for_level():
    req_data = request.get_json()
    print(req_data)
    input_password = req_data['password']
    input_level = int(req_data['level'])
    print(req_data)
    print(f"password_attempt: {input_password}")
    if input_level >= len(data['system_arr']) or input_level < 0:
        return jsonify({"success": False, "assistant": "incorrect level! are you trying to fool me, hackerit? xd"})
    # check if the password is correct for the current level
    if input_password != data['passwords_arr'][input_level-1]: # -1 since 1st level is at index 0 so pass[0]
        return {"success": False, "assistant": "Incorrect Password!"}
    # if password correct
    else:
        if input_level + 1 >= len(data['system_arr']):
            return {"success": True, "assistant": "You finished ALL THE CHALLENGES! OMG SUCH Hackerit!", "system": "You finished ALL THE CHALLENGES! OMG SUCH Hackerit!"}
        else:
            next_challenge_system = data['system_arr'][input_level + 1]
            return {"success": True, "assistant": "Password correct!! Next level..", "system": next_challenge_system}

# Get prompt+level and check for solution
@app.route('/api/attempt', methods=['POST'])
@cross_origin()
def check_solution():
    req_data = request.get_json()
    input_prompt = req_data['prompt']
    input_level = req_data['level']
    if input_level >= len(data['system_arr']):
        return jsonify({"success": False, "message": "incorrect level! are you trying to fool me, hackerit? xd"})
    response = send_prompt_get_response(input_level,input_prompt)
    return response


# TODO - validate this!
# get level - good for 1st one
@app.route('/api/level', methods=['POST'])
@cross_origin()
def get_prompt():
    req_data = request.get_json()
    print(f"req_DATA: {req_data}")
    input_level = int(req_data['level'])
    if not input_level:
        return jsonify({"success": False, "message": "No level was submitted!"})
    if input_level < 1 or input_level >= len(data['system_arr']):
        return jsonify({"success": False, "message": "Invalid level! Are you trying to fool me, Hackerit? XD"})
    return jsonify({'system': data['system_arr'][input_level - 1]}), 200 # -1 since we count from 0 index in array

# TODO - default error handler to prevent server crash

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333)

