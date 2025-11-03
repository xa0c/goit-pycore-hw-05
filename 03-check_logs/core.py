import logging
from datetime import datetime
from collections import defaultdict

LINE_MAX_SIZE = 10000
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR"]
LOG_COLUMN_COUNT = 4
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
COLUMN_NAMES = ["Log Level", "Count"]

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def load_logs(file_path: str) -> list:
    """Read log file into a list of parsed records.

    Args:
        file_path (str): Path to the source file.

    Returns:
        list: List of parsed log records.

    Raises:
        OSError: If file can't be read.
        UnicodeDecodeError: If file has wrong UTF-8 encoding.
    """
    records = []
    line_number = 0
    try:
        with open(file_path, mode="r", encoding="utf-8", errors="strict") as fh:
            # Safe line-by-line read with line length limitation
            for line in iter(lambda: fh.readline(LINE_MAX_SIZE), ""):
                line_number += 1
                try:
                    # Parse current line and append to the final list
                    records.append(parse_log_line(line))
                except ValueError as e:
                    logging.warning(f"Skipping line #{line_number}. Reason: {e}")
                    continue
    except OSError as e:
        raise OSError(f"File `{file_path}` can't be read.") from e
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"File `{file_path}` has wrong UTF-8 encoding.") from e

    return records


def parse_log_line(line: str) -> dict:
    """Parse line from log file into dict values.

    Date/time columns must be a valid date and match DATETIME_FORMAT \
        format. Log level column must be one of LOG_LEVELS.

    Args:
        line (str): Raw line from log file.

    Returns:
        dict: Dict with datetime object, log level string and message.

    Raises:
        ValueError:
            - If line has incomplete set of columns.
            - If date/time columns have invalid format or value.
            - If log level column has invalid value.
    """
    # Limit max split count by LOG_COLUMN_COUNT constant to avoid log message splitting
    record = line.rstrip("\r\n").split(maxsplit=LOG_COLUMN_COUNT-1)

    # Line must consist of LOG_COLUMN_COUNT columns
    if len(record) < LOG_COLUMN_COUNT:
        raise ValueError("Incomplete set of columns.")

    # Parse date and time columns
    try:
        dt = datetime.strptime(f"{record[0]} {record[1]}", DATETIME_FORMAT)
    except ValueError as e:
        raise ValueError("Date/time columns have invalid format or value.") from e

    # Validate log level column
    if record[2] not in ("DEBUG", "INFO", "WARNING", "ERROR"):
        raise ValueError("Log level column has invalid value.")

    return {"datetime": dt, "level": record[2], "message": record[3]}


def filter_logs_by_level(logs: list, level: str) -> list:
    """Filter log records by log level.

    Args:
        logs (list): List of log records.
        level (str): Log level.

    Returns:
        list: List of log records filtered by specified log level.
    """
    return [r for r in logs if r["level"] == level]


def count_logs_by_level(logs: list) -> dict:
    """Calculate counts of log records by log level.

    Args:
        logs (list): List of log records.

    Returns:
        dict: Dict of discovered log levels and their records counts.
    """
    results = defaultdict(int)
    for record in logs:
        results[record["level"]] += 1
    return results


def display_log_counts(counts: dict):
    """Print table with log levels and correspending records counts.

    Table is sorted by "Count" value (descending).

    Args:
        counts (dict): Dict with log levels and corresponding counts.
    """
    # Desc sorting by Count value
    counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)

    # Calculate needed width for the 1st column
    max_column_width = max(len(COLUMN_NAMES[0]), max([len(x[0]) for x in counts])) + 1
    # Print header with border
    print(COLUMN_NAMES[0].ljust(max_column_width) + "│ " + COLUMN_NAMES[1])
    print("─" * max_column_width + "┼─" + "─" * len(COLUMN_NAMES[1]))
    # Print records
    for level, count in counts:
        print(level.ljust(max_column_width) + "│ " + str(count))
