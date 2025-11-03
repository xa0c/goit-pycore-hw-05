import readline
import core

MSG_HELP = """\
DESCRIPTION:
    This script provides CLI for contact management.

USAGE:
    - add <person> <value>
        Validates content of <value> and adds contact record for the specified person. Rewrite \
isn't allowed.
    - change <person> <value>
        Rewrites phone contact record for the specified person.
    - phone <person>
        Prints person's phone number.
    - all [ <person> ]
        If person is specified, prints person's contact.
        Otherwise prints complete contacts database.
    - help
        Prints this message.
    - hello
        Prints "hello" message.
    - exit | close
        Quits application.

NOTES:
    Person name can contain spaces."""

MSG_BAD_ARG_COUNT = "Wrong number of arguments. Use -h flag to read about command usage."


def parse_input(user_input: str) -> tuple[str, dict[str, str]]:
    """Parse string into a tuple of command name and its arguments.

    Args:
        user_input (str): Input string.

    Returns:
        tuple[str, dict[str, str]]: Tuple of command name and a
            dictionary of it's arguments.

    Raises:
        ValueError: If user input has wrong number of arguments.
    """
    if not user_input:
        return "", {}

    cmd, *args = user_input.strip().split()
    match cmd:
        case "add" | "change":
            if len(args) < 2:
                raise ValueError(MSG_BAD_ARG_COUNT)
            args = {"name": " ".join(args[:-1]), "value": args[-1]}
        case "phone":
            if len(args) < 1:
                raise ValueError(MSG_BAD_ARG_COUNT)
            args = {"name": " ".join(args)}
        case "all":
            args = {} if len(args) == 0 else {"name": " ".join(args)}

    return cmd.lower(), args


def main():
    print(MSG_HELP)

    while True:
        # Handle empty input, interrupts and parse errors
        try:
            cmd = input("> ")
            if not cmd:
                continue
            cmd, args = parse_input(cmd)
        except (KeyboardInterrupt, EOFError):
            print("\nProgram interrupted by user.")
            break
        except ValueError as e:
            print("ERROR:", e, "Try again.")
            continue

        # Store functions for easier command handling
        cmd_funcs = {
            "add": core.add_contact,
            "change": core.change_contact,
            "phone": core.show_phone,
            "all": core.render_person_table,
        }

        # Handle commands
        match cmd:
            case "exit" | "close":
                print("Exiting program. Good bye!")
                break
            case "hello":
                print("Hello! How can I help you?")
            case "help":
                print(MSG_HELP)
            case "add" | "change" | "phone" | "all":
                print(cmd_funcs[cmd](**args))
            case _:
                print("ERROR: Unknown command. Try again.")


if __name__ == "__main__":
    main()
