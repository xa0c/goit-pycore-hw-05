import sys
import core

ARGS_MIN_COUNT = 1
ARGS_MAX_COUNT = 2
MSG_HELP = """\
USAGE:
    python main.py <file_path> [ <level> ]

DESCRIPTION:
    This script parses log file from the 1st argument and prints record count statistics by level.
    If 2nd "level" argument is provided then script additionally outputs log records filtered by \
provided level value.
    File `test.log` is shipped together with this script for testing purposes."""


def parse_args(argv: list) -> tuple[str, str]:
    """Parse argv list into a tuple of file path and log level.

    Args:
        argv (list): Argument list from sys.argv value.

    Returns:
        tuple[str, str]: Tuple of file path and log level.

    Raises:
        ValueError:
            - If wrong number of arguments was passed.
            - If log level value is invalid.
    """
    args = argv[1:]

    # Check if number of passed arguments matches requirements
    if len(args) < ARGS_MIN_COUNT or len(args) > ARGS_MAX_COUNT:
        raise ValueError("Wrong number of arguments.")

    # Extend list of arguments with "None" values for those which are missing
    args.extend([None] * (ARGS_MAX_COUNT - len(args)))

    # Validate log level argument
    if args[1]:
        args[1] = args[1].upper()
        if args[1] not in core.LOG_LEVELS:
            raise ValueError("Log level value is invalid.")

    return tuple(args)


def main():
    # Parse args and save values in variables
    try:
        file_path, level = parse_args(sys.argv)
    except ValueError as e:
        print(f"ERROR: {e} Try again.\n\n{MSG_HELP}")
        return -1

    # Load log file and parse log records
    try:
        records = core.load_logs(file_path)
    except (OSError, UnicodeDecodeError, ValueError) as e:
        print(f"ERROR: {e}")
        return -1

    # Create dict with record counts by level
    counts = core.count_logs_by_level(records)

    # Print table with stats
    core.display_log_counts(counts)

    # Print log records if level was specified
    if level:
        print(f"\nLog details for the level '{level}':")
        for record in core.filter_logs_by_level(records, level):
            print(f"{record["datetime"]:{core.DATETIME_FORMAT}} - {record["message"]}")


if __name__ == "__main__":
    main()
