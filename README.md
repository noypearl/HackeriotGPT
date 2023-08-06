# HackeriotGPT Prompt Jailbreak
ChatGPT jailbreak game that was made specifically for [Hackeriot conference](https://www.hackeriot.org/), 
for a workshop that I did together with [Gadi Evron](https://twitter.com/gadievron)

<img width="400" alt="hackeriot-screenshot" src="https://github.com/noypearl/HackeriotGPT/assets/11259340/bb34141a-bd06-4572-a8d5-2b92fc17bedb">

<br>

<img width="600" alt="workshop" src="https://github.com/noypearl/HackeriotGPT/assets/11259340/12f60570-06ed-4a7f-9ed7-a31a8fca8c5d">

Hackeriot GPT Prompt Attack is a web-based game designed to challenge and educate users about the intricacies of GPT-4 prompt hacking. The game is built using Python Flask for the backend and HTML/CSS/JavaScript for the frontend.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. Make sure to replace the API key with your own. Notice that each API call will cost you money - read more [here](https://openai.com/pricing) <br>
<br>
<img width="400" alt="image" src="https://github.com/noypearl/HackeriotGPT/assets/11259340/aa670b88-af62-4cf0-9a01-765bf0fee437">


## Structure
<img width="400" alt="project-structure" src="https://github.com/noypearl/HackeriotGPT/assets/11259340/aaef3748-6f5d-42a1-ab87-68c4e55d496d">

### Prerequisites

- Python 3.7 or higher
- Flask
- A modern web browser

### Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/noypearl/HackeriotGPT.git
```

Navigate to the project directory:
```bash
cd HackeriotGPT
```

Install the required Python packages:
```bash
pip install -r requirements.txt
```

Register to OpenAI and [get an API key to use](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)
Create environment (.env) and put the following (replace the value with your real key):
```
OPENAPI_KEY=YOUR_REAL_OPENAPI_KEY
```
If there are issues with the environment variable - [look at this line and change it accordingly](https://github.com/noypearl/HackeriotGPT/blob/main/app.py#L18C1-L19C1)

Run the Application
Start the Flask server:
```bash
flask run
```

Open your web browser and navigate to http://localhost:5000.


### Usage
The game presents a series of levels, each with a unique GPT-4 prompt hacking challenge. 
The user must input the correct responses to advance through the levels.

#### HACK THE PLANET!

<img width="400" alt="doggo" src="https://github.com/noypearl/HackeriotGPT/assets/11259340/78897471-5d82-489b-a63a-b1babda7c797">



