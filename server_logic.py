"""Shows functions of server list, find by name, add, remove filter by environment, validation"""

VALID_ENVIRONMENTS = ["dev", "test", "prod"]

def find_server(servers, name):
    """Finds a server with the given name, none if not found"""
    for server in servers:
        if server["name"] == name:
            return server
    return None
