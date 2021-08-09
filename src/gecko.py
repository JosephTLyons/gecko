import time

from functools import wraps
from typing import Callable


def disable(func: Callable) -> Callable:
    """This decorator prevents the function it decorates from executing"""
    @wraps(func)
    def wrapper(*args, **kwargs):  # TODO: type annotations for this function
        print(f"{func.__name__} is disabled")

    return wrapper


def retry(exceptions: tuple[type[BaseException], ...], number_of_retries: int, duration_between_retries_in_seconds: float) -> Callable:
    """This decorator re-calls the function it decorates when the function raises any `Exception` in the `exceptions` tuple.
    It should be noted that the function is called once before any retries are attempted.  Because of this,
    the number of times the function will be called will be `number_of_retries` + 1.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):  # TODO: type annotations for this function
            retry_count = 0

            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as exception:
                    if retry_count < number_of_retries:
                        retry_count += 1
                        time.sleep(duration_between_retries_in_seconds)
                    else:
                        raise exception
                except Exception as exception:
                    raise exception

        return wrapper

    return decorator
