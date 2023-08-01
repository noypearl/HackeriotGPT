import json

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import random
import string

app = Flask(__name__)

CORS(app) # TODO - fix this when I'm alive!
# gpt = GPT(engine="text-davinci-002", temperature=0.5)
MODEL = "gpt-3.5-turbo" # TODO - check if there's a cheaper mode (?)
messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]
# Store the passwords for each level
# passwords = ["Hackeriot" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) for _ in range(13)]
passwords_arr = ["Hackeriot" + str(_) for _ in range(13)]
print(f"passwords: {passwords_arr}")

with open("levels.json", "r") as f:
    levels_json = json.load(f)
system = levels_json['system']

# notice levels are starting from 1 in GUI + REST API!
data = {'passwords_arr': passwords_arr, 'assistant_arr': levels_json['assistant'], 'system_arr': levels_json['system']}

# return response according to prompt + level
# def send_prompt_get_response(level, prompt):
#     openai.ChatCompletion.create(
#        model=MODEL,
#        messages=[
#        {"role": "system","content": data['system_arr'][level-1]},
#        {"role": "user", "content": prompt}
#        ]
#     )

#     )

# Send level + password and try to get next challenge!
@app.route('/api/checkpass', methods=['POST'])
def check_password_for_level():
    req_data = request.get_json()
    input_password = req_data['password']
    input_level = req_data['level']
    print(f"password_attempt: {input_password}")
    if input_level >= len(data['system_arr']):
        return jsonify({"success": False, "message": "incorrect level! are you trying to fool me, hackerit? xd"})
    # check if the password is correct for the current level
    if input_password != data['passwords_arr'][input_level-1]: # -1 since 1st level is at index 0 so pass[0]
        return jsonify({"success": False, "message": "invalid password."})
    else:
        # omg levels finished!
        if input_level == len(data['system_arr']) - 1:
            return jsonify({"success": True, "message": "omg you're a 1337 hacker! you completed all the levels!!"}) # todo - try to finish the last level to test this line
        # should return next system
        else:
            return jsonify({"success": True, "message": "Password correct! Going to next level!",
                            "system": data['system_arr'][input_level+1]})

# Get prompt+level and check for solution
@app.route('/api/attempt', methods=['POST'])
def check_solution():
    req_data = request.get_json()
    input_prompt = req_data['prompt']
    input_level = req_data['level']
    if input_level >= len(data['system_arr']):
        return jsonify({"success": False, "message": "incorrect level! are you trying to fool me, hackerit? xd"})


# TODO - validate this!
# get level - good for 1st one
@app.route('/api/level', methods=['POST'])
def get_prompt():
    req_data = request.get_json()
    input_level = req_data['level']
    if not input_level:
        return jsonify({"success": False, "message": "No level was submitted!"})
    if input_level < 1 or input_level >= len(data['system_arr']):
        return jsonify({"success": False, "message": "Invalid level! Are you trying to fool me, Hackerit? XD"})
    return jsonify({'system': data['system_arr'][input_level - 1]}), 200 # -1 since we count from 0 index in array

# TODO - default error handler to prevent server crash

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

