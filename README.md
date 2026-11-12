# Server Inventory Tool

A command-line tool for keeping track of servers and checking whether they respond.
The program stores a list of servers in a JSON file, can ping one or all of them, saves
the result and time of each check, and exports a report as CSV.

It can be used in two ways:

- **Menu mode:** an interactive text menu, started without any arguments.
- **CLI mode:** single commands with flags, suited for scripts and pipelines. Each command
  exits with an exit code that tells whether it succeeded.

> **Note on naming:** the whole project is written in English, including the data file,
> the JSON keys, the environment variable, the report folder and the command-line flags.
> See [Names compared with the assignment](#names-compared-with-the-assignment) for how
> they map to the names in the assignment.

## Requirements

- **Python 3.10 or later.** The program only uses Python's standard library, so there is
  nothing to install with `pip`.
- **Linux, macOS or WSL (Windows Subsystem for Linux).** The checks run the operating
  system's `ping` command with Linux-style flags (`-c` and `-W`). On plain Windows, use
  WSL. On a minimal Linux install, `ping` may need to be installed first:

  ```bash
  sudo apt install iputils-ping
  ```

## Getting started

```bash
git clone https://github.com/sidneytellman/Server_Inventory_Tool.git
cd Server_Inventory_Tool
python3 main.py
```

The repository includes `server.json` with four example servers, so the program has data
to work with straight away.

## Menu mode

Start the program without any arguments:

```bash
python3 main.py
```

The menu is shown again after every choice, until you choose `0`.

| Option | What it does |
|---|---|
| 1 | List all servers in a table |
| 2 | List the servers in one environment (`dev`, `test` or `prod`) |
| 3 | Add a new server (status starts as `unknown`) |
| 4 | Remove a server |
| 5 | Check one server |
| 6 | Check all servers |
| 7 | Export a report as CSV |
| 0 | Exit |

Behaviour worth knowing:

- **Invalid input** never crashes the program. An unknown menu choice, an unknown server
  name or an invalid environment gives a clear message. When adding a server, you are
  asked for the environment again until you enter a valid one.
- **Server names must be unique.** Adding a server with a name that already exists is
  refused.
- **Removing a `prod` server** needs an extra confirmation: you have to type `yes`.
- **Every change is saved straight away** to the data file, so nothing is lost if the
  program is closed.

## CLI mode

Each command runs once and then exits.

```bash
python3 main.py --help                        # show all options
python3 main.py --list                        # list all servers
python3 main.py --list --environment prod     # list only the prod servers
python3 main.py --check web01                 # check one server
python3 main.py --check-all                   # check all servers
python3 main.py --export                      # export a CSV report
```

`--environment` only accepts `dev`, `test` or `prod`. Any other value is rejected with a
message from `argparse`.

### Exit codes

| Command | Exit code 0 | Exit code 1 |
|---|---|---|
| `--list`, `--export` | Always | – |
| `--check NAME` | The server is up | The server is down, or the name does not exist |
| `--check-all` | Every server is up | At least one server is down |

You can see the exit code of the last command with `echo $?`:

```bash
python3 main.py --check-all; echo $?
```

This is what lets the tool be used in a script or pipeline, for example to stop a
deployment if a server does not respond.

## The data file and `INVENTORY_DATA_FILE`

By default the program reads and writes `server.json` in the folder it is started from.
To use a different file, set the environment variable `INVENTORY_DATA_FILE`:

```bash
# For a single run
INVENTORY_DATA_FILE=test.json python3 main.py --list

# For the rest of the terminal session
export INVENTORY_DATA_FILE=test.json
python3 main.py
```

This makes it possible to keep separate files, for example one for testing, without
changing any code. A safe way to try the program without touching the real data:

```bash
cp server.json test.json
INVENTORY_DATA_FILE=test.json python3 main.py
```

If the file does not exist, the program starts with an empty list instead of crashing.
The file is created the first time something is saved.

### File format

The data file is a JSON list where each server is an object with six values, all of them
strings:

```json
[
  {
    "name": "web01",
    "address": "example.com",
    "environment": "prod",
    "role": "webserver",
    "status": "unknown",
    "last_checked": ""
  }
]
```

| Key | Description |
|---|---|
| `name` | Unique name of the server |
| `address` | Domain name or IP address to ping |
| `environment` | `dev`, `test` or `prod` |
| `role` | What the server is used for, for example `webserver` or `database` |
| `status` | `up`, `down` or `unknown` (new servers start as `unknown`) |
| `last_checked` | Time of the latest check as `YYYY-MM-DD HH:MM`, empty if never checked |

## How the checks work

A check runs `ping -c 1 -W 2 <address>`: one packet, with a two-second timeout. If ping
gets a reply, the server is marked `up`, otherwise `down`. The time of the check is saved
in `last_checked`, and the data file is updated.

Two of the example servers behave in a known way:

- `test01` (`192.0.2.10`) is an address reserved for documentation and never answers, so
  it is always `down`. Its check takes about two seconds because of the timeout.
- `db01` (`127.0.0.1`) and `dev01` (`localhost`) are the local machine and are always `up`.

## CSV reports

`--export`, or option 7 in the menu, writes all servers to a CSV file in the `reports/`
folder, for example:

```
reports/server_report_2026-11-12_1045.csv
```

The file has a header row and one row per server, and opens directly in Excel or Google
Sheets. The `reports/` folder is created automatically if it does not exist, and it is
listed in `.gitignore`, so generated reports are never committed.

## Project structure

```
Server_Inventory_Tool/
├── main.py            # Starting point: reads the flags with argparse, starts the menu or runs a CLI command
├── menu.py            # The text menu: the menu loop and one function per menu option
├── server_logic.py    # Shared logic for the server list: find, add, remove, filter, validate, print
├── checks.py          # Checks whether servers respond, using ping via subprocess
├── storage.py         # Files: reads the data file name, loads and saves JSON, exports CSV
├── server.json        # The server data
├── README.md          # This file
├── REDOGORELSE.md     # Written explanation of the code
├── REFLEKTION.md      # Reflection on design choices
└── .gitignore         # Keeps __pycache__/ and reports/ out of Git
```

`main.py` and `menu.py` only handle input and output. All the real work is done in
`server_logic.py`, `checks.py` and `storage.py`, and both modes call the same functions,
so no logic is written twice.

## Names compared with the assignment

The assignment uses Swedish names. This project uses English names throughout:

| In the assignment | In this project |
|---|---|
| `servrar.json` | `server.json` |
| `INVENTORY_DATAFIL` | `INVENTORY_DATA_FILE` |
| `rapporter/` | `reports/` |
| `--lista` | `--list` |
| `--miljo` | `--environment` |
| `--kontrollera` | `--check` |
| `--kontrollera-alla` | `--check-all` |
| `--export` | `--export` |
| `namn`, `adress`, `miljo`, `roll`, `status`, `senast_kontrollerad` | `name`, `address`, `environment`, `role`, `status`, `last_checked` |
| `meny.py`, `lagring.py`, `kontroller.py` | `menu.py`, `storage.py`, `checks.py` |