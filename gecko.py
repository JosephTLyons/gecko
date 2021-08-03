from functools import wraps
from typing import Any, Callable


def disable(func: Callable) -> Callable:
    """This decorator simply keeps whatever function it decorates from executing"""

    @wraps(func)
    def wrapper(*args: list[Any], **kwargs):
        print(f"{func.__name__} is disabled")

    return wrapper
