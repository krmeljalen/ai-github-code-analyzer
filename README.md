# ai-rating
AI rating application that checks out your github repos, analyzes the code and gives you some feedback.

## Prerequirements
Have ollama running on localhost, make sure you downloaded your model ie. llama3.1:8b

## Install
run pipenv install

## Running
Edit the config.yaml and modify the repo that you wish to parse, it should be publicly visible, so code can clone it and run: python main.py

At this point you are free to ask AI about your code to give you feedback on it. 

Enjoy!
