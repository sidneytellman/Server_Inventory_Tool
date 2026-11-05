"""Shows the user a menu of options to choose from, reads the user input and calls the appropriate function"""

import storage
import checks
import server_logic


def print_menu():
    """Prints the menu of options for the user."""
    print("\nServer Management Menu:")
    print("1. List all servers")
    print("2. List servers by environment")
    print("3. Add a new server")
    print("4. Remove a server")
    print("5. Check server status")
    print("6. Check all servers status")
    print("7. Export report as CSV")
    print("0. Exit")


def ask_for_environment():
    """Asks the user for an environment and validates it."""
    while True:
        environment = input("Enter the environment (dev, test, prod): ").strip().lower()
        try:
            server_logic.validate_environment(environment)
            return environment
        except ValueError as error:
            print(error)


def menu_list_by_environment(servers):
    """Asks for an environment and lists servers in it."""

    environment = ask_for_environment()
    filtered_servers = server_logic.filter_servers_by_environment(servers, environment)
    if filtered_servers:
        server_logic.print_servers(filtered_servers)
    else:
        print(f"No servers found in the '{environment}' environment.")


def menu_add_server(servers, data_file):
    """Asks for server details and adds a new server."""

    name = input("Enter server name: ").strip()
    address = input("Enter server address: ").strip()
    environment = ask_for_environment()
    role = input("Enter the server role: ").strip()

    try:
        new_server = server_logic.add_server(servers, name, address, environment, role)
    except ValueError as error:
        print(error)
        return

    storage.save_servers(servers, data_file)
    print(f"Server '{new_server['name']}' added successfully.")





def run_menu(): 
    """Runs the menu, reading user input, calling appropriate functions until user choose to exit"""
    data_file = storage.get_data_file()
    servers = storage.load_servers(data_file)

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            server_logic.print_servers(servers)
        elif choice == "2":
            menu_list_by_environment(servers)
        elif choice == "3":
            menu_add_server(servers, data_file)
        elif choice == "4":
            menu_remove_server(servers, data_file)
        elif choice == "5":
            menu_check_server(servers, data_file)
        elif choice == "6":
            menu_check_all_servers(servers, data_file)
        elif choice == "7":
            menu_export_csv(servers)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, select a number from the menu.")