from functools import wraps
from typing import Any, Callable


def disable(func: Callable) -> Callable:
    """This decorator prevents the function it decorates from executing"""

    @wraps(func)
    def wrapper(*args, **kwargs):  # TODO: type annotations for args
        print(f"{func.__name__} is disabled")

    return wrapper
