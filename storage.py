"""Reads and saves JSON, exports CSV"""

import json
import csv
import os
from pathlib import Path
from datetime import datetime

DEFAULT_DATA_FILE = "server.json"

def get_data_file():
    """returns the data file name from INVENTORY_DATAFIL, or the default."""
    return os.environ.get("INVENTORY_DATAFIL", DEFAULT_DATA_FILE)


def load_servers(data_file):
    """Loads server data from the JSON file. Returns an empty list if file does not exist"""
    if not Path(data_file).exists():
        return []
    with open(data_file, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_servers(servers, data_file):
    """Saves the list of servers to the JSON file."""
    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(servers, file, indent=4, ensure_ascii=False)