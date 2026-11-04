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

