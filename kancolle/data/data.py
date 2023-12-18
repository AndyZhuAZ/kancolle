"""Data module."""
import json
from os import path

import requests  # type: ignore

from kancolle.data import KC_DATA_URL, MODULE_PATH

session = requests.Session()


def download():
    """Download ship, ship type, and ship class data and save to JSON."""
    file_data = {
        "ship.json": "ship/ship.json",
        "shiptype.json": "shiptype/all.json",
        "shipclass.json": "shipclass/all.json",
    }

    for filename, _path in file_data.items():
        url = KC_DATA_URL + _path
        data = session.get(url).json()
        save_data(data, filename)


def save_data(data, file_name):
    """This function saves a given data into a specified file.

    Args:
        data (dict): The data to be saved. It should be a dictionary.
        file_name (str): The name of the file where the data will be saved.

    Returns:
        None
    """
    file_name = path.join(MODULE_PATH, file_name)
    with open(file_name, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))


def load_data(file_name):
    """Load data from file.

    Args:
        file_name (str): file name

    Returns:
        dict
    """
    file_name = path.join(MODULE_PATH, file_name)
    with open(file_name, 'r') as f:
        return json.loads(f.read())


def load_ship_data():
    """Load ship data."""
    return load_data("ship.json")


def load_ship_type_data():
    """Load ship type data."""
    return load_data("shiptype.json")


def load_ship_class_data():
    """Load ship class data."""
    return load_data("shipclass.json")


if __name__ == '__main__':
    download()
