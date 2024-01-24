import sys
from pathlib import Path
import pyfiglet
import cowsay
from prompt_toolkit import prompt
from utility.addressbook import AddressBook
from utility.addressbook_inter import *
from utility.cmd_complet import CommandCompleter, similar_command
from user_interface import UserInterface 
from console_interface import ConsoleInterface


program_dir = Path(__file__).parent
ADDRESSBOOK_DATA_PATH = program_dir.joinpath("data/addressbook.dat") 


ADDRESSBOOK = AddressBook().load_addressbook(ADDRESSBOOK_DATA_PATH)
    
user_interface = ConsoleInterface()     ## mod

# function to handle with errors
def error_handler(func):
    def wrapper(*args):
        while True:
            try:
                return func(*args)
            except FileNotFoundError as e: 
                return f"I can't find folder."
            except KeyboardInterrupt:
                cli_pyassist_exit()
    return wrapper


# a function that parses user input commands
def parse_command(user_input: str) -> (str, tuple):
    tokens = user_input.split()
    command = tokens[0].lower()
    arguments = tokens[1:]
    return command, tuple(arguments)


# taking a command from the user
def user_command_input(completer: CommandCompleter, menu_name=""):
    user_input = prompt(f"{menu_name} >>> ", completer=completer).strip()
    if user_input:
        return parse_command(user_input)
    return "", ""
    

# exit / close program
def cli_pyassist_exit(*args): 
    ADDRESSBOOK.save_addressbook(ADDRESSBOOK_DATA_PATH)
    cowsay.daemon("Your data has been saved.\nGood bye!") 
    sys.exit()


# function to show menus addressbook & notes
def show_menu(menu_options):
    max_option_length = max(len(item['option']) for item in menu_options) 
    print("Options:".ljust(max_option_length + 5), "Command:")
    print("-" * (max_option_length + 24))
    for _, item in enumerate(menu_options):
        print(f"{item['option'].ljust(max_option_length + 5)} {item['command']}")
    print("-" * (max_option_length + 24))


# function to handle addressbook command
def addressbook_commands(*args):
    menu_options = [
        {"option": "Show All Records", "command": "show"},
        {"option": "Show Specific Record", "command": "show <name>"},
        {"option": "Add Record", "command": "add"},
        {"option": "Edit Record", "command": "edit"},
        {"option": "Delete Record", "command": "delete"},
        {"option": "Search in Addressbook", "command": "search <query>"},
        {"option": "Upcoming Birthdays", "command": "birthday <days>"}, # (selected number of days ahead) - informacja do instrukcji 
        {"option": "Export Address Book", "command": "export"},
        {"option": "Import Address Book", "command": "import"},
        {"option": "Main Menu", "command": "up"}, 
        {"option": "Program exit", "command": "exit"},
        {"option": "Show this Menu", "command": "help"},
    ]
    show_menu(menu_options)
    completer = CommandCompleter(list(ADDRESSBOOK_MENU_COMMANDS.keys()) + list(ADDRESSBOOK.keys()))
    while True:
        cmd, arguments = user_interface.user_command_input(None, "address book")    ## mod
        user_interface.display_message(execute_commands(ADDRESSBOOK_MENU_COMMANDS, cmd, ADDRESSBOOK, arguments)) ## mod


# dict for main menu handler
MAIN_COMMANDS = {
    "exit": cli_pyassist_exit,
    "addressbook": addressbook_commands,
}


@error_handler
def pyassit_main_menu(*args):
    menu_options = [
        {"option": "Open your address book", "command": "addressbook"},
        {"option": "Open your notes", "command": "notes"},
        {"option": "Sort files in <directory>", "command": "sort <directory>"}, 
        {"option": "Program exit", "command": "exit"},
        {"option": "Show this Menu", "command": "help"},
    ]
    show_menu(menu_options)
    completer = CommandCompleter(MAIN_COMMANDS.keys())
    while True:
        cmd, arguments = user_interface.user_command_input(None, "main menu") ## mod
        user_interface.display_message(execute_commands(MAIN_COMMANDS, cmd, None, arguments)) ## mod
# dict for addressbook menu
ADDRESSBOOK_MENU_COMMANDS = {
    "exit": cli_pyassist_exit,
    "add": add_record,
    "edit": edit_record,
    "show": show,
    "delete": del_record, 
    "export": export_to_csv,
    "import": import_from_csv, 
    "birthday": show_upcoming_birthday, 
    "search": search, 
    "up": pyassit_main_menu,
}

    
def execute_commands(menu_commands: dict, cmd: str, data_to_use, arguments: tuple):
    if cmd not in menu_commands:
        return f"Command {cmd} is not recognized" + similar_command(cmd, menu_commands.keys())
    cmd = menu_commands[cmd]
    return cmd(data_to_use, *arguments)


def main():
    print(pyfiglet.figlet_format("PyAssist", font = "slant"))
    pyassit_main_menu()
    

if __name__ == "__main__":
    main()