import json
import sys
import os

def get_config():
    if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/../config.json"):
        sys.exit("'config.json' not found.")
    else:
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/../config.json") as file:
            config = json.load(file)
            return config
    return None

def get_config_value(key):
    config = get_config()
    return config.get(key)