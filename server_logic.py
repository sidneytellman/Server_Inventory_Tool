"""Shows functions of server list, find by name, add, remove filter by environment and print."""

VALID_ENVIRONMENTS = ["dev", "test", "prod"]


def validate_environment(environment):
    """Validates if the environment is valid. Raises ValueError if not."""
    if environment not in VALID_ENVIRONMENTS:
        raise ValueError(f"Invalid environment: {environment}. Valid environments are: {', '.join(VALID_ENVIRONMENTS)}")


def find_server(servers, name):
    """Finds a server with the given name, none if not found"""
    
    for server in servers:
        if server["name"] == name:
            return server
    return None


def get_server(servers, name):
    """Returns the server with the given name, raises ValueError if not found"""
    server = find_server(servers, name)
    if server is None:
        raise ValueError(f"Server with name '{name}' not found.")
    return server



def filter_servers_by_environment(servers, environment):
    """Filters servers by the given environment. Returns a list of servers in that environment."""
    validate_environment(environment)
    
    filtered_servers = []
    for server in servers:
        if server["environment"] == environment:
            filtered_servers.append(server)
    return filtered_servers


def add_server(servers, name, address, environment, role):
    """Adds a new server with status unknown. Raises ValueError if the name is taken or the environment is invalid."""
    if find_server(servers, name) is not None:
        raise ValueError(f"Server with name '{name}' already exists.")
    validate_environment(environment)

    new_server = {
        "name": name,
        "address": address,
        "environment": environment,
        "role": role,
        "status": "unknown",
        "last_checked": ""
    }
    servers.append(new_server)
    return new_server


def remove_server(servers, name):
    """Removes a server by name. Raises ValueError if the server is not found."""
    server = find_server(servers, name)
    if server is None:
        raise ValueError(f"Server with name '{name}' not found.")
    servers.remove(server)
    return server 


def print_servers(servers):
    """Prints the servers as a table that is aligned"""
    if not servers:
        print("No servers to display.")
        return

    print(f"{'Name':<20} {'Address':<20} {'Environment':<12} {'Role':<20} {'Status':<10} {'Last Checked':<20}")
    print("-" * 108)
    for server in servers:
        print(f"{server['name']:<20} {server['address']:<20} {server['environment']:<12} {server['role']:<20} {server['status']:<10} {server['last_checked']:<20}")
