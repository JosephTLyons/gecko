import time

from functools import wraps
from typing import Any, Callable, TypeVar, cast


# https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
Func = TypeVar("Func", bound=Callable[..., Any])


def disable(should_print_details: bool = False) -> Callable[[Func], Func]:
    def decorator(func: Func) -> Func:
        """This decorator prevents the function it decorates from executing."""
        @wraps(func)
        def wrapper(*args, **kwargs):  # type: ignore
            if should_print_details:
                print(f"{func.__name__} is disabled")

        return cast(Func, wrapper)

    return decorator


def retry(
    *exceptions: type[BaseException],
    number_of_retries: int = 3,
    duration_between_retries_in_seconds: float = 1,
    should_print_details: bool = False
) -> Callable[[Func], Func]:
    """
    This decorator re-calls the function it decorates when the function raises any `Exception` in the `exceptions` tuple.
    It should be noted that the function is called once before any retries are attempted.  Because of this,
    the number of times the function will be called will be `number_of_retries` + 1.
    """
    def decorator(func: Func) -> Func:
        @wraps(func)
        def wrapper(*args, **kwargs):  # type: ignore
            # We must loop an additional time to ensure that the `else` block can be executed
            for retry_count in range(number_of_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exception:
                    if retry_count < number_of_retries:
                        time.sleep(duration_between_retries_in_seconds)

                        if should_print_details:
                            print(f"{func.__name__}: retry {retry_count + 1}")
                    else:
                        raise exception

        return cast(Func, wrapper)

    return decorator
