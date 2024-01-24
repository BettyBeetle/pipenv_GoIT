from abc import ABC, abstractmethod

class UserInterface(ABC):
    @abstractmethod
    def show_menu(self, menu_options):
        pass

    @abstractmethod
    def user_command_input(self, completer, menu_name=""):
        pass

    @abstractmethod
    def display_message(self, message):
        pass