import re
from collections.abc import Callable
from decimal import Decimal


def generator_numbers(text: str) -> Decimal:
    """Yield number from provided text.

    Args:
        text (str): Source text.

    Yields:
        Decimal: Extracted number.
    """
    # Iterate through lightweigh str.split() call results
    for word in text.split():
        # Check if "word" matches real number regex and yield Decimal value
        if re.fullmatch(r"\d+(\.\d+)?", word):
            yield Decimal(word)


def sum_profit(text: str, func: Callable) -> Decimal:
    """Calculate sum of all generated values from provided text.

    Args:
        text (str): Source text.
        func (Callable[[str], Decimal]): Numbers generator.

    Returns:
        Decimal: Total sum of generated values.
    """
    return sum(func(text))


if __name__ == "__main__":
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, \
доповнений додатковими надходженнями 27.45 і 324.00 доларів."

    total_income = sum_profit(text, generator_numbers)
    print(f"Total income: {total_income}")
