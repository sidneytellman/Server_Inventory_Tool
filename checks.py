"""Checks whether servers are responding"""

import subprocess


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