import pygsheets
import pandas as pd
from werkzeug.exceptions import RequestTimeout
from threading import Thread
import json
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import openai
import os
import string

# initialize Google Sheet and get 1st page
def init_gsheet():
    gc = pygsheets.authorize(service_account_env_var="GOOGLE_CREDS")
    # Create empty dataframe
    df = pd.DataFrame()
    # open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sh = gc.open('HackeriotGPT Game')
    #select the first sheet
    return sh[0]

def append_to_sheet(sheet, type_value, value, name=""):
    """
    Appends a new row to the Google Sheet.

    Parameters:
    - type_value (str): Either 'password' or 'prompt'
    - value (str): The value of the password or prompt
    """
    # Append data to the sheet
    sheet.append_table([type_value, value, name])

app = Flask(__name__)

CORS(app) # TODO - fix this when I'm alive!
PREMESSAGE = "The password is ████. "
# MODEL = "gpt-3.5-turbo" # TODO - check if there's a cheaper mode (?)
MODEL = "gpt-3.5-turbo" # TODO - check if there's a cheaper mode (?)
messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]
OPENAPI_KEY = os.environ.get('OPENAPI_KEY')
GOOGLE_CREDS = os.environ.get('GOOGLE_CREDS')  # optional
MAX_LEVELS=21
# Store the passwords for each level
# passwords = ["Hackeriot" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) for _ in range(13)]
passwords_arr = ["H4ckerIoT", "hackeriotIsCOOL", "w3Ar3Hack3riot", "breakingCHATHackeriot", "HackForFun","myGPTisBetterThanYours","WhatAmIHacking","lolImHacker","h4ck3ed","GPT-FTW","woohooCyber","CyberHackeriot","HackeriotAI" , "WatDeHack?", "IMTheHackerit", "GPTIsS0Easy","GPTLovesHackerit", "EliteHackeritGPT", "HackeritGPTChamp", "TooEasyForHackerit", "FinishedOMGHackerit"]
print(f"passwords: {passwords_arr}")
wks = ''
if GOOGLE_CREDS:
    wks = init_gsheet()

with open("levels.json", "r") as f:
    levels_json = json.load(f)
system_arr = levels_json['system']

# notice levels are starting from 1 in GUI + REST API!
data = {'passwords_arr': passwords_arr, 'assistant_arr': levels_json['assistant'], 'system_arr': system_arr, 'initial': levels_json['initial']}


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
    # adding support in 21 levels
    if level > 13:
        assistant_message = next((item[str(level)] for item in data['assistant_arr'] if str(level) in item),
                                      None)  # Todo  validate alignment
        gpt_messages.append({"role": "assistant", "content": assistant_message})
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAPI_KEY}'
    }
    body = {
        'model': MODEL,
        'messages': gpt_messages,
        'temperature': 0
    }
    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(body))
        response_data = response.json()
        assistant_response = response_data['choices'][0]['message']['content']
        next_challenge_system = data['system_arr'][level+1]
        if level > 13:
            # TODO - debug it
            next_challenge_system += next((item[str(level)] for item in data['assistant_arr'] if str(level) in item), None) # Todo  validate alignment
        return {"success": True, "assistant": assistant_response, "system": PREMESSAGE + next_challenge_system }
    except RequestTimeout:
        return jsonify({"success": False, "assistant": "Request timed out"})

# Send level + password and try to get next challenge!
@app.route('/api/checkpass', methods=['POST'])
@cross_origin()
def check_password_for_level():
    try:
        req_data = request.get_json()
        print(req_data)
        input_password = req_data['password']
        input_level = int(req_data['level'])
        print(req_data)
        print(f"password_attempt: {input_password}")
        if GOOGLE_CREDS:
            append_to_sheet(wks, "password", input_password) # TODO - add name optionally
        if input_level > MAX_LEVELS or input_level < 0:
            return jsonify({"success": False, "assistant": "incorrect level! are you trying to fool me, hackerit? xd"})
        # check if the password is correct for the current level
        if input_password != data['passwords_arr'][input_level-1]: # -1 since 1st level is at index 0 so pass[0]
            return {"success": False, "assistant": "Incorrect Password!"}
        # if password correct
        else:
            if input_level + 1 >= MAX_LEVELS:
                return {"success": True, "assistant": "You finished ALL THE CHALLENGES! OMG SUCH Hackerit!", "system": "You finished ALL THE CHALLENGES! OMG SUCH Hackerit!"}
            else:
                next_challenge_system = PREMESSAGE + data['system_arr'][input_level + 1]
                if input_level > 13:
                    next_challenge_system += next((item[str(input_level)] for item in data['assistant_arr'] if str(input_level) in item),None)  # Todo  validate alignment
                return {"success": True, "assistant": "Password correct!! Next level..", "system": next_challenge_system}
    except RequestTimeout:
        return jsonify({"success": False, "assistant": "Request timed out"})

# Get prompt+level and check for solution
@app.route('/api/attempt', methods=['POST'])
@cross_origin()
def check_solution():
    try:
        req_data = request.get_json()
        input_prompt = req_data['prompt']
        input_level = int(req_data['level'])
        print(f"input_level: {input_level}")
        if GOOGLE_CREDS:
            append_to_sheet(wks, "prompt", input_prompt)# TODO - add name optionally
        if input_level > MAX_LEVELS:
            return jsonify({"success": False, "assistant": "incorrect level! are you trying to fool me, hackerit? xd"})
        response = send_prompt_get_response(input_level,input_prompt)
        return response
    except RequestTimeout:
        return jsonify({"success": False, "assistant": "Request timed out"})


# TODO - validate this!
# get level - good for 1st one
@app.route('/api/level', methods=['POST'])
@cross_origin()
def get_prompt():
    try:
        req_data = request.get_json()
        input_level = int(req_data['level'])
        print(f"input_level: {input_level}")
        if not input_level:
            return jsonify({"success": False, "message": "No level was submitted!"})
        if input_level < 1 or input_level > MAX_LEVELS:
            return jsonify({"success": False, "message": "Invalid level! Are you trying to fool me, Hackerit? XD"})
        if input_level > 13:
            system_message = PREMESSAGE + next((item[str(input_level)] for item in data['assistant_arr'] if str(input_level) in item), None)
        else:
            system_message = PREMESSAGE + data['system_arr'][input_level - 1]
        return jsonify({'system': system_message }), 200 # -1 since we count from 0 index in array
    except RequestTimeout:
        return jsonify({"success": False, "message": "Request timed out"})


# TODO - default error handler to prevent server crash


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run(host='0.0.0.0', port=3333)


