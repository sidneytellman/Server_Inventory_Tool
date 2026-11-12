### 1. Three constructs in the program

conditions: `load_servers()` in `storage.py`

In the `storage.py` module I have defined a function called `load_servers()` that takes one parameter, `data_file`, which is the path to the JSON file. The if statement checks whether the file that `data_file` points to exists.`Path(data_file)` turns the file name into a path object, and `.exists()` returns `True` if the file is there and `False` if it
is not. `not` flips that value, so the indented line under the colon only runs when the file is missing. `return []` then ends the function straight away with an empty list, so the code further down that opens the file never runs.**

If the file exists, the function opens it and reads the JSON. With an empty list, the
program starts with no servers, and the file is only created the first time you save,
for example by adding a server.

The interesting part of this function is the guard clause
`if not Path(data_file).exists(): return []`. It ensures that the program does not crash. Without the check, trying to open or read a non-existing file would result in a `FileNotFoundError` and the program would stop running entirely. Having a guard clause means the program can keep on functioning without crashing.

### Loop: `check_all_servers()` in `checks.py`

In `checks.py`, `check_all_servers()` uses a loop to find out whether every server in the list is up. It starts with a flag, `all_up = True`, which assumes that all servers are up until one proves otherwise. The loop `for server in servers:` goes through the list one server at a time, and in each round `server` holds that server's dictionary. Each server is checked with `check_server(server)`. If the check returns `False`, the flag is flipped to `False`, and since nothing flips it back, one server being down is enough to change the result.

`return all_up` sits at the same level as `for`, so it only runs once the loop has gone through the whole list. `main.py` then uses the result to set the exit code for `--check-all`: 0 if every server is up, and 1 if at least one is down.

### Function with parameter and return: `ping_host()` in `checks.py` 

`ping_host(address)` is a function that determines whether a network host (a domain name or IP address) is reachable. `def ping_host(address):` defines the function with one parameter, `address`, which receives the address from the server's dictionary. It works by running the operating system's `ping` tool from within Python, and returns `True` if the host responds and `False` otherwise.

`subprocess` is the module that lets Python run commands on the operating system, and `subprocess.run()` is the function that runs them. The command is written as a list where each argument has its own role: `"ping"` calls the ping tool, `"-c", "1"` sends only one packet so it does not keep running, `"-W", "2"` is a two-second timeout so the program does not freeze if the host is offline, and `address` is the target. Because each part is passed separately and no shell is used, the address cannot be interpreted as extra commands, even if it contains characters like ;. `capture_output=True` stores the command's output in `result` instead of printing it in the terminal.

The `try/except` catches a `FileNotFoundError`, which Python raises if the `ping` program is not installed. Instead of crashing, the function returns `False`. Finally,
`result.returncode` is the command's exit code: 0 means the ping got a reply, and anything else means it failed. `== 0` compares the two, so the function returns `True` or `False`
directly. `check_server()` calls `ping_host()` and uses that answer to set the server's status to `"up"` or `"down"`.

### 2. Why a list of dictionaries? 

Each server is a dictionary and like a database all the servers are in a list where the list is a table and each dictionary is a row. Having this list makes it easy to add, remove and loop through servers like `add_server()` and `remove_server()` in `server_logic.py` do with `append()` and `remove()`. All six values are strings (`str`), including the IP address. `last_checked` is an empty
string until `check_server()` in `checks.py` sets it to a timestamp.

### 3. Why save the data as a JSON but export the report as a CSV

Json keeps the structure and can be read straight back into a list of dictionaries. `load_servers()`() `save_servers()` in `storage.py` only need `json.dump()` and `json.load()`. The reason to export it as a CSV is it's meant to be easily readbale for people, it's a flat tablle that opens directly in excel or Google sheets. CSV would not be the best fit for storage as it has no structure beyond rows and columns and every value reads back as text. 

### 4. How the program is split and responsibilities

The programs starting point is `main.py`, the `parse_arguments()` read the commans-line flags with `argparse`, and `main()` either starts the menu or runs a CLI command and exits with the correct exit code. 

`menu.py` module handles the text menu. `run_menu()` runs the loop and one small funtion per option, for example `menu_add_server()` and `menu_check_server()` asks for input and calls the other modules. 

`server_logic.py` is what holds the shared logic for the server list, `find_server()`,
`get_server()`, `add_server()`, `remove_server()`, `filter_servers_by_environment()`,
`validate_environment()` and `print_servers()`.

`checks.py` what this does is to check if servers respond, `ping_host()`, `check_server()` and
`check_all_servers()`.

`storage.py` is there to handle files, `get_data_file()`, `load_servers()`, `save_servers()` and
`export_csv()`.

`menu.py` and `main.py` these are there to handle input and output and function by calling the same functions in the other three modules. An example of that is that both menu and `--check` use `get_server()` and `check_server()`, so that logic is only written once.

### 5. Which modules from the standard library do you use, and what for?

The program only uses modules from pythons standard library that way ensuring nothing beyond python itself needs to be installed. 

- `os` is used in `get_data_file()` in `storage.py` where it reads the `INVENTORY_DATA_FILE` variable and falls back to `server.json` if it is not set.
- `json` is used in `load_servers()` and `save_servers()` in `storage.py` where `json.load()` reads the data file into a list of dictionaries and `json.dump()` writes it back. 
- `csv` is used in `export_csv()` in `storage.py`, where `csv.DictWriter` writes the report
with a header row followed by one row per server.
- `pathlib` is used in `load_servers()` and `export_csv()` in `storage.py`, where `Path(...).exists()` checks whether the data file exists and `mkdir()` creates the `reports/` folder if it is missing.
- `datetime` is used in `export_csv()` in `storage.py` and `check_server()` in `checks.py`, where `datetime.now().strftime()` creates the timestamp in the report's file name and in `last_checked`.
- `subprocess` is used in `ping_host()` in `checks.py`, where `subprocess.run()` runs the operating system's `ping` command.
- `argparse` is used in `parse_arguments()` in `main.py`, where it defines the command-line flags and automatically creates the `--help` text.
- `sys` is used in `main()` in `main.py`, where `sys.exit()` ends the program with exit code 0 if everything went fine and 1 if a server is down or not found.

### 6. Three examples of good practice. 

I approached the project thinking of prior work experience and how readable my code is. One thing i tried to focus on was not having any duplicated logic which turned out to be a challenge. I have rules that are needed in several places that are written once and called from other areas. `validate_environment()` in `server_logic.py` is used both by `add_server()` and by `filter_servers_by_environment()`, and `get_server()` is used both by the menu (`menu_check_server()`, `menu_remove_server()`) and by `--check` in `main.py`. If a rule needs to change, it only has to be changed in one place, and the menu and the CLI can never behave differently.

The command as a list in `subprocess.run()`. In `ping_host()` in `checks.py`, I wrote the ping command as a list, `["ping", "-c", "1", "-W", "2", address]`, instead of one string. The reason for this is that no shell is used, so an address containing characters like `;` cannot run extra commands. Adding the `-W 2` timeout also ensures that an offline server can't make the program hang.

Saving after every change. `storage.save_servers()` is called directly after each change in `menu_add_server()`, `menu_remove_server()`, `menu_check_server()` and `menu_check_all_servers()` in `menu.py`, and after `--check` and `--check-all` in `main.py`. If the program crashes or is closed, nothing that has already been done is lost. 

### 7. Sources used and why I used them. 

While working on this project I used a number of different sources to help me during periods where I felt stuck or faced an issue. The presentations we're of great use when it came to understanding the standard libraries, lists, loops and especially JSON. Having some slight experience with JSON but not in a comprehensive way, going through the slides was of great use to get a more concrete understanding of it and how it would come to be of use during this project. 
I also read up on python documentation(docs.python.org) mainly in regards to `argparse` which took a while to really get a grasp of. Having such a resource available was of great help and helped break it down in a digestible way. Alongside that I used Claude(AI tool) to help break down each section of the project, create checklists of what to work on, code reviewing(for example indentation errors
and a misspelled environment variable) and a general structure. 
I also had some friends and classmates help look over certain parts of the program to give feedback on what is missing or what I can do differently for example who suggested moving repeated logic into a function that is called from several places instead of how I had been working up to that point. 