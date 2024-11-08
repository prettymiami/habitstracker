import json

DATAFILE = "data.json"

def load_data():
    try:
        with open(DATAFILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open(DATAFILE, 'w') as file:
        json.dump(data, file)
