import difflib
from prompt_toolkit.completion import Completer, Completion  # pip install prompt_toolkit


def similar_command(user_cmd: str, commands: list) -> str:
    matches = difflib.get_close_matches(user_cmd, commands)
    if matches:
        return f"\nmaybe you meant: {' or '.join(matches)}"
    return ""


class CommandCompleter(Completer):
    def __init__(self, commands: list):
        self.commands = commands

    def get_completions(self, text, complete_event):
        word_before_cursor = text.get_word_before_cursor()
        matches = [cmd for cmd in self.commands if cmd.startswith(word_before_cursor)]
        if not matches:                                                                         
            close_matches = difflib.get_close_matches(word_before_cursor, self.commands) 
            if close_matches:                                                                   
                match = close_matches[0]
                yield Completion(match, start_position=-len(word_before_cursor))                      
        else:
            for match in matches:                                                               
                yield Completion(match, start_position=-len(word_before_cursor))