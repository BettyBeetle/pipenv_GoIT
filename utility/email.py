import re
from utility.field import Field


class Email(Field):
    """
    class for email object

    Args:
        Field (class): parent class
    """

    # function used as a decorator to catch errors when value is setting
    def _value_error(func):
        def inner(self, email):
            while True:
                email = email.strip()
                if re.search(
                    r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
                    email,
                ):
                    return func(self, email)
                else:
                    raise ValueError

        return inner

    @_value_error
    def __init__(self, value: str) -> None:
        self._value = value

    # Getter for value
    @property
    def value(self):
        return self._value

    # Setter for value
    @value.setter
    @_value_error
    def value(self, value: str):
        self._value = value
