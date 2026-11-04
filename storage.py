"""Reads and saves JSON, exports CSV"""

import json
import csv
import os
from pathlib import Path
from datetime import datetime

DEFAULT_DATA_FILE = "server.json"
CSV_FIELDS = ["name", "address", "environment", "role", "status", "last_checked"]

def get_data_file():
    """returns the data file name from INVENTORY_DATA_FILE, or the default."""
    return os.environ.get("INVENTORY_DATA_FILE", DEFAULT_DATA_FILE)


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

def export_csv(servers):
    """Exports all servers to a timestamped CSV file and returns it's path."""
    report_folder = Path("reports")
    report_folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    csv_file_path = report_folder / f"server_report_{timestamp}.csv"
    
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(servers)

    return csv_file_path