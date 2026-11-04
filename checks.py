"""Checks whether servers are responding"""

import subprocess
from datetime import datetime


def ping_host(address):
    """Pings the given address once. Returns true if it responds, otherwise false."""
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", address],
            capture_output=True,
        )
    except FileNotFoundError:
        return False
    return result.returncode == 0

def check_server(server):
    """Checks if the server is responding and updates its status and last_checked."""
    is_responding = ping_host(server["address"])
    server["status"] = "up" if is_responding else "down"
    server["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return is_responding
