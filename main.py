"""reads arguments with argparse and chooses between menu and CLI"""

import argparse
import sys
import checks
import menu
import server_logic
import storage


def parse_arguments():
    """Defines the command line arguments and returns the parsed arguments."""
    parser = argparse.ArgumentParser(description="Server Inventory Tool")
    parser.add_argument("--list", action="store_true", help="List all servers and exit.")
    parser.add_argument("--environment", choices=server_logic.VALID_ENVIRONMENTS, help="Only list servers in this environment (use with --list).")
    parser.add_argument("--check", metavar="NAME", help="Check one server by name and exit.")
    parser.add_argument("--check-all", action="store_true", help="Check all servers and exit.")
    parser.add_argument("--export", action="store_true", help="Export the server report as CSV and exit.")
    return parser.parse_args()


def main():
    """Starts the menu if no arguments are given, runs CLI command otherwise"""
    args = parse_arguments()

    if not (args.list or args.check or args.check_all or args.export):
        menu.run_menu()
        return

    data_file = storage.get_data_file()
    servers = storage.load_servers(data_file)

    if args.list:
        if args.environment:
            servers_to_show = server_logic.filter_servers_by_environment(servers, args.environment)
        else:
            servers_to_show = servers
        server_logic.print_servers(servers_to_show)
        sys.exit(0)

    elif args.check:
        try:
            server = server_logic.get_server(servers, args.check)
        except ValueError as error:
            print(error)
            sys.exit(1)
        is_up = checks.check_server(server)
        storage.save_servers(servers, data_file)
        print(f"Server '{server['name']}' status: {server['status']}, last checked: {server['last_checked']}")
        sys.exit(0 if is_up else 1)

    elif args.check_all:
        all_up = checks.check_all_servers(servers)
        storage.save_servers(servers, data_file)
        server_logic.print_servers(servers)
        sys.exit(0 if all_up else 1)

    elif args.export:
        file_path = storage.export_csv(servers)
        print(f"Servers exported to CSV file: {file_path}")
        sys.exit(0)
        

if __name__ == "__main__":
    main()