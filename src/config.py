import json
import sys


def get_json(filename: str):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        sys.exit(filename + " not found")


def get_config():
    return get_json("config.json")


def get_paths():
    return get_json("path-config.json")


def get_key_config():
    return get_json("key-config.json")
