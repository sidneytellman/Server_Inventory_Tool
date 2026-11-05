"""Shows functions of server list, find by name, add, remove filter by environment, validation"""

VALID_ENVIRONMENTS = ["dev", "test", "prod"]

def find_server(servers, name):
    """Finds a server with the given name, none if not found"""
    
    for server in servers:
        if server["name"] == name:
            return server
    return None


def filter_servers_by_environment(servers, environment):
    """Filters servers by the given environment"""

    if environment not in VALID_ENVIRONMENTS:
        raise ValueError(f"Invalid environment: {environment}. valid environments are: {', '.join(VALID_ENVIRONMENTS)}")

    filtered_servers = []
    for server in servers:
        if server["environment"] == environment:
            filtered_servers.append(server)
    return filtered_servers
    
