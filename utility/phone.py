from utility.field import Field


class Phone(Field):
    """
    class for phone number object

    Args:
        Field (class): parent class
    """

    # function used as a decorator to catch errors when value is setting
    def _value_error(func):
        def inner(self, value):
            while True:
                value = (
                    value.strip()
                    .removeprefix("+")
                    .replace("(", "")
                    .replace(")", "")
                    .replace("-", "")
                    .replace(" ", "")
                )
                if not value.isnumeric():
                    raise ValueError
                else:
                    return func(self, value)

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
