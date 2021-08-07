from functools import wraps
from typing import Callable


def disable(func: Callable) -> Callable:
    """This decorator prevents the function it decorates from executing"""
    @wraps(func)
    def wrapper(*args, **kwargs):  # TODO: type annotations for this function
        print(f"{func.__name__} is disabled")

    return wrapper
