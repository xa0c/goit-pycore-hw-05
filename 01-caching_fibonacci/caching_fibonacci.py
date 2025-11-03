from collections.abc import Callable


def caching_fibonacci() -> Callable[[int], int]:
    """Return cache-enabled Fibonacci function.

    Returns:
        Callable[[int], int]: Cache-enabled Fibonacci function.
    """
    # Init dict for cached values
    cache = {}

    def fibonacci(n: int) -> int:
        """Calculate Fibonacci value for the N-th element.

        Args:
            n (int): Fibonacci position.

        Returns:
            int: Value for the N-th element.

        Raises:
            ValueError: If input is negative number.
        """
        if n < 0:
            raise ValueError("Negative values aren't supported.")

        # Hardcoded returns for 0 and 1
        if n < 2:
            return n

        # Update cache if N-th value is absent
        if not cache.get(n):
            cache[n] = fibonacci(n-1) + fibonacci(n-2)

        # Return value from cache
        return cache[n]

    return fibonacci


if __name__ == "__main__":
    # Create a closure function
    fib = caching_fibonacci()

    # Calculate Fibonacci values
    print(fib(10))  # Outputs 55
    print(fib(15))  # Outputs 610
