import os
import csv
from .record import Record
from .phone import Phone
from .email import Email
from .birthday import Birthday, FutureDateError
from .address import Address
from .name import Name
from .addressbook import AddressBook
from prompt_toolkit import prompt
from utility.cmd_complet import CommandCompleter, similar_command




# function to handle with errors
def error_handler(func):
    def wrapper(*args):
        while True:
            try:
                return func(*args)
            except ValueError:
                if func.__name__ == "add_name":
                    print("The name field cannot be empty, try again.")
                if func.__name__ == "add_phone":
                    print("Invalid phone number, try again.")
                if func.__name__ == "add_email":
                    print("Invalid email, try again.")
                if func.__name__ == "add_birthday":
                    print("Invalid date format, try again.")
                if func.__name__ == "import_from_csv":
                    return "I can't import from this source. Check the file."
                if func.__name__ == "show_upcoming_birthday":
                    return "Wrong number of days to show. Please try again."
            except FutureDateError:
                print("You can't use a future date as a birthday, try again.")
            except FileNotFoundError:
                if func.__name__ == "export_to_csv":
                    return "Error: Unable to find the specified file. Please try again."
                if func.__name__ == "import_from_csv":
                    return "Error: Unable to find the specified file. Please try again."
            except Exception as e:
                return f"Error: {e}. Please try again."
    return wrapper


@error_handler
def add_name(addressbook) -> Name:
    while True:
        name = input("Type name or <<< if you want to cancel: ").strip().title()
        if name in addressbook.keys():
            print(f"Contact {name} already exists. Choose another name.")
            continue
        elif name == "<<<":
            return None
        return Name(name)


@error_handler
def add_phone():
    phone = input("Type phone or <<< if you want to cancel: ")
    if phone == "<<<":
        return None
    return Phone(phone)


@error_handler
def add_email():
    email = input("Type email or <<< if you want to cancel: ")
    if email == "<<<":
        return None
    return Email(email)


@error_handler
def add_birthday():
    birthday = input("Input the date of birth as day month year (e.g. 15-10-1985 or 15 10 1985) or <<< if you want to cancel: ")
    if birthday == "<<<":
        return None
    return Birthday(birthday)    
    

#@error_handler
def add_address():
    street = input("street: ")
    city = input("city: ")
    zip_code = input("zip code: ")
    country = input("country: ")
    return Address(street, city, zip_code, country)


def create_record(name):
    phones = []
    emails = []
    birthday = None
    address = None
    while True:
        answer = (input("Type Y (yes) if you want to add phone number: ").strip().lower())
        if answer == "y" or answer == "yes":
            while True:
                phone = add_phone()
                if phone is not None:
                    phones.append(phone)
                    answer = (input("Type Y (yes) if you want to add another phone number: ").strip().lower())
                    if answer == "y" or answer == "yes":
                        continue
                break
        break
    
    while True:
        answer = input("Type Y (yes) if you want to add email: ").strip().lower()
        if answer == "y" or answer == "yes":
            while True:
                email = add_email()
                if email is not None:
                    emails.append(email)
                    answer = (input("Type Y (yes) if you want to add another email: ").strip().upper())
                    if answer == "y" or answer == "yes":
                        continue
                break
        break
    
    answer = input("Type Y (yes) if you want to add birthday: ").strip().lower()
    if answer == "y" or answer == "yes":
        birthday = add_birthday()
    
    answer = input("Type Y (yes) if you want to add address: ").strip().lower()
    if answer == "y" or answer == "yes":
        address = add_address()
    
    return Record(name, phones, emails, birthday, address)


@error_handler
def add_record(addressbook, *args):
    if len(args) == 0:
        name = add_name(addressbook)      
    else:
        name = " ".join(args).strip().title()
        if name in addressbook.keys():
            print(f"Contact {name} already exists. Choose another name.")
            name = add_name(addressbook) 
        else:
            name = Name(name)
    if name is not None:
        record = create_record(name)
        addressbook.add_record(record)
        return f"A record: {record} added to your address book."
    return "Operation cancelled"


def del_record(addressbook, *args):
    if not args:
        name = input("Enter the name of the record you want to delete: ").strip().title()
    else:
        name = " ".join(args).strip().title()

    if name in addressbook:
        del addressbook[name]
        return f"Record {name} deleted successfully."
    else:
        return f"Record {name} not found in the address book."
    

def show(addressbook, *args):
    if not args:
        for info in addressbook.iterator():
            print(info, end="")
            if info:
                input("Press Enter to continue.")
        return "" 
    name_record_to_show = " ".join(args).strip().title()
    if name_record_to_show in addressbook:
        return f"{addressbook[name_record_to_show]}"
    return f"Contact {name_record_to_show} doesn't exist."

@error_handler 
def export_to_csv(addressbook, *args):
    while True:
        if not args:
            filename = input("Type the filename to export to (e.g., output.csv) or <<< to cancel: ").strip()
        else:
            filename = "".join(args)        
        if filename == "<<<" or filename == "":
            return "Export cancelled."
        data_directory = os.path.join(os.getcwd(), "data")
        os.makedirs(data_directory, exist_ok=True)
        full_path = os.path.join(data_directory, filename)
        addressbook.export_to_csv(full_path)
        return f"Data exported successfully to {full_path}."


@error_handler         
def import_from_csv(addressbook, *args):
    if not args:
        filename = input("Enter the CSV file name for import: ").strip()
    else:
        filename = "".join(args)
    if filename == "<<<" or filename == "":
            return "Import cancelled."
    addressbook.import_from_csv(filename)
    return f"Data imported successfully from {filename}."


#function displays the birthdays of contacts in the next days. If the user has not entered a number of days, the function displays for 7 days.
@error_handler
def show_upcoming_birthday(adressbook, *args):
    if not args:
        number_of_days = 7
    else:
        number_of_days = int("".join(args))
        if number_of_days < 1:
            raise ValueError
    info = f"Upcoming birthdays in the next {number_of_days} days:"
    is_upcoming_birthday = False
    for day, records in adressbook.records_with_upcoming_birthday(number_of_days).items():
        if records: # if the list for the day is not empty
            names = []
            for record in records:
                names.append(record.name.value)    
            info += "\n{:>10}, {:<18}: {:<60}".format(day.strftime('%A'), day.strftime('%d %B %Y'), '; '.join(names))
            is_upcoming_birthday = True
    if is_upcoming_birthday:
        return info
    return f"No upcoming birthdays in the next {number_of_days} days."


# edit existing name
def edit_name(addressbook, record):
    print(f"Type new name for contact {record.name}")
    new_name = add_name(addressbook)
    if new_name:
        addressbook.add_record(Record(new_name, record.phones, record.emails, record.birthday, record.address))
        old_record = addressbook.pop(record.name.value)
        return f"Name changed from {old_record.name} to {new_name}"
    return "Operation canceled."

    
# changing birthday
@error_handler
def edit_birthday(addressbook, record):
    birthday = add_birthday()
    if birthday:
        addressbook[record.name.value].birthday = birthday
        return f"{record.name} birthday set to: {birthday}"
    return "Operation canceled."


@error_handler
def edit_address(addressbook, record):
    record.address = add_address() # na razie najprostsza wersja, do czasu zmiany walidacji w klasie Address
    return f"{record.name} new {record.address}"


# init function for phone changed
@error_handler
def edit_phone(addressbook, record):
    return change_data(record, "phone")

# init function for email changed
@error_handler
def edit_email(addressbook, record):
    return change_data(record, "email")    


# help menu function to choose email or phone
def item_selection(record, data_list, show):
    print(f"Contact {record.name} {type}s:\n{show}", end="")
    number_to_change = input("Select by typing a number (for example 1 or 2): ")
    try:
        number_to_change = int(number_to_change) - 1
        if number_to_change >= len(data_list) or number_to_change < 0:
            raise ValueError
        return number_to_change
    except ValueError:
        return -1
    
        
# change of phone or email
def change_data(record, type):
    if type == "phone":
        data_list = record.phones
        show = record.show_phones()
        add_type = record.add_phone
    elif type == "email":
        data_list = record.emails
        show = record.show_emails()
        add_type = record.add_email
    while True:
        if len(data_list) > 0:
            while True:
                answer = input(f"Contact {record.name} {type}s:{show}\nDo you want change it or add another? 1 chanege, 2 add, 3 delete: ")
                if answer == "1":
                    if len(data_list) == 1:
                        data_to_add = add_email() if type == "email" else add_phone()
                        if data_to_add is not None:
                            data_list[0] = data_to_add
                            return f"{type} edited sucessfully."
                        return "Operation canceled."
                    else:
                        number_to_change = item_selection(record, data_list, show)
                        if number_to_change == -1:
                            print("Wrong option, try again")
                            break
                        data_to_add = add_email() if type == "email" else add_phone()
                        if data_to_add is not None:
                            data_list[number_to_change] = data_to_add
                            return f"{type} edited sucessfully."
                        return "Operation canceled."
                elif answer == "2":
                    data_to_add = add_email() if type == "email" else add_phone()
                    if data_to_add is not None:
                        add_type(data_to_add)
                        return f"{type} edited sucessfully."
                    return "Operation canceled."
                elif answer == "3":
                    if len(data_list) == 1:
                        data_list.clear()
                        return f"{type} edited sucessfully."
                    else:
                        number_to_delete = item_selection(record, data_list, show)
                        if number_to_delete == -1:
                            print("Wrong option, try again")
                            break
                        print(f"{type} no {number_to_delete+1}: {data_list.pop(number_to_delete)} deleted.")
                        return f"{type} edited sucessfully."
                else:
                    print("Unrecognized command, try again.")
        else:
            data_to_add = add_email() if type == "email" else add_phone()
            if data_to_add:
                add_type(data_to_add)
                return f"{type} edited sucessfully."
            return "Operation canceled."


# dict for menu edit handler
EDIT_COMMANDS = {
    "name": edit_name, 
    "phone": edit_phone, 
    "email": edit_email,
    "address": edit_address,
    "birthday": edit_birthday,
    }


def execute_commands(commands: dict, cmd: str, addressbook: AddressBook, record: Record):
    """
    Function to execute user commands

    Args:
        menu_commands (dict): dict for menu-specific commands
        cmd (str): user command
        arguments (tuple): arguments from user input

    Returns:
        func: function with arguments
    """
    if cmd not in commands:
        return f"Command {cmd} is not recognized" + similar_command(cmd, commands.keys())
    cmd = commands[cmd]
    return cmd(addressbook, record)


# record edit
def edit_record(addressbook, *args):
    name_completer = CommandCompleter(addressbook.keys())
    command_completer = CommandCompleter(EDIT_COMMANDS)
    if not args:
        name = prompt("Enter the name of the record you want to edit: ", completer=name_completer).strip().title()
    else:
        name = " ".join(args).strip().title()
    if name in addressbook:
        record = addressbook[name]
        menu_options = [
        {"option": "Edit Name", "command": "name"},
        {"option": "Edit Phone", "command": "phone"},
        {"option": "Edit Email", "command": "email"},
        {"option": "Edit Address", "command": "address"},
        {"option": "Edit Birthday", "command": "birthday"},
    ]

        max_option_length = max(len(item['option']) for item in menu_options) 
        
        print("Options:".ljust(max_option_length + 5), "Command:")
        print("-" * (max_option_length + 15))

        for index, item in enumerate(menu_options):
            print(f"{item['option'].ljust(max_option_length + 5)} {item['command']}")

        print("-" * (max_option_length + 15))
        command = prompt(f"Type what you want to change in {name} contact: ", completer=command_completer)
        print(execute_commands(EDIT_COMMANDS, command, addressbook, record))
        return "<<<"
    else:
        return f"Record {name} not found in the address book."
    

# method to search addressbook
def search(addressbook, *args):
    if not args:
        search_query = input("Enter the search query (or type '<<<' to exit): ").strip()
        if search_query == "<<<":
            return "Operation canceled."
    else:
        search_query = " ".join(args).strip()
    results = addressbook.search(search_query)
    if results:
        print("Search results:")
        return show(results)
    else:
        return "No matching results found."