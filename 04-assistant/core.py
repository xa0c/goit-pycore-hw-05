import functools
from collections.abc import Callable

E_INVALID_FORMAT = "Invalid phone format: only digits are allowed."
E_PERSON_NOT_EXISTS = "Specified person doesn't exist."
E_PHONE_DUPLICATE = "Specified phone number exists for another person."

persons = {}


def input_error(func: Callable) -> Callable:
    """Decorator that catches exceptions and returns them from function

    Args:
        func (Callable): Function to wrap.

    Returns:
        Callable: Wrapped function with same signature.
    """
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError) as e:
            return f"ERROR: {e.args[0]} Try again."
    return inner


@input_error
def add_contact(name: str, value: str) -> str:
    """Add phone contact record to the specified person.

    Args:
        name (str): Person's name.
        value (str): Phone number value.

    Returns:
        string: Operation result message.

    Raises:
        KeyError: If contact already exists for the specified person.
        ValueError:
            - If contact value has invalid format.
            - If contact value isn't unique.
    """
    # Don't allow to overwrite existing contact value
    if persons.get(name) is not None:
        raise KeyError("Phone number is already configured for this person. Use `change` command.")

    # Check if provided phone number consists of ASCII digits
    if not (value.isascii and value.isdigit()):
        raise ValueError(E_INVALID_FORMAT)

    # Check if provided contact value is unique
    phone_number = int(value)
    if phone_number in persons.values():
        raise ValueError(E_PHONE_DUPLICATE)

    persons[name] = phone_number
    return "Phone contact added."


@input_error
def change_contact(name: str, value: str) -> str:
    """Rewrite person's contact new value.

    Args:
        name (str): Person's name.
        value (str): Phone number value.

    Returns:
        string: Operation result message.

    Raises:
        KeyError: If person doesn't exist.
        ValueError:
            - If contact value has invalid format.
            - If contact value isn't unique.
    """
    # Check if provided person exists
    if persons.get(name) is None:
        raise KeyError(E_PERSON_NOT_EXISTS)

    # Check if provided phone number consists of ASCII digits
    if not (value.isascii and value.isdigit()):
        raise ValueError(E_INVALID_FORMAT)

    # Check if provided contact value is unique (excluding current person)
    phone_number = int(value)
    if phone_number in [p[1] for p in persons.items() if p[0] != name]:
        raise ValueError(E_PHONE_DUPLICATE)

    persons[name] = phone_number
    return "Phone contact updated."


@input_error
def show_phone(name: str) -> str:
    """Return phone number for the specified person.

    Args:
        name (str): Person's name.

    Returns:
        str: Person's phone number.

    Raises:
        KeyError: If person doesn't exist.
    """
    # Check if provided person exists
    try:
        phone = persons[name]
    except KeyError as e:
        raise KeyError(E_PERSON_NOT_EXISTS) from e

    return str(phone)


@input_error
def render_person_table(name: str = None) -> str:
    """Render person's table of contacts.

    Renders single person if name is provided. Otherwise renders all.

    Args:
        name (str): Person's name.

    Returns:
        str: Rendered person's table of contacts.

    Raises:
        KeyError: If person doesn't exist.
    """
    render_dict = persons
    if name:
        # Check if provided person exists
        try:
            render_dict = {name: persons[name]}
        except KeyError as e:
            raise KeyError(E_PERSON_NOT_EXISTS) from e

    # Build output
    output = ""
    for name, contact in render_dict.items():
        output += "/" + '═' * 30 + "\\\n"
        output += "│" + f"{name}".center(30) + "│\n"
        output += "├" + "─" * 30 + "┤\n"
        output += "│" + f" Phone: {contact}".ljust(30) + "│\n"
        output += "└" + "─" * 30 + "┘\n"

    return output
