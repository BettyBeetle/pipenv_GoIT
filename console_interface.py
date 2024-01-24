from user_interface import UserInterface

class ConsoleInterface(UserInterface):
    def show_menu(self, menu_options):
        max_option_length = max(len(item['option']) for item in menu_options)
        print("Options:".ljust(max_option_length + 5), "Command:")
        print("-" * (max_option_length + 24))
        for _, item in enumerate(menu_options):
            print(f"{item['option'].ljust(max_option_length + 5)} {item['command']}")
        print("-" * (max_option_length + 24))

    def user_command_input(self, completer, menu_name=""):
        return input(f"{menu_name} >>> ").strip(), ""

    def display_message(self, message):
        print(message)