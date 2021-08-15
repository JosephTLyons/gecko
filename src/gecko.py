import time

from functools import wraps
from typing import Any, Callable, TypeVar, cast, get_type_hints


# https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
Func = TypeVar("Func", bound=Callable[..., Any])


def disable(func: Func) -> Func:
    """This decorator prevents the function it decorates from executing"""
    @wraps(func)
    def wrapper(*args, **kwargs):  # type: ignore
        print(f"{func.__name__} is disabled")

    return cast(Func, wrapper)


def retry(*exceptions: type[BaseException], number_of_retries: int = 3, duration_between_retries_in_seconds: float = 1) -> Callable[[Func], Func]:
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
                    else:
                        raise exception

        return cast(Func, wrapper)

    return decorator


def validate(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        type_hints = get_type_hints(function)

        expected_types = list(type_hints.values())

        for actual_argument_value, expected_type in zip(args, expected_types):
            if not isinstance(actual_argument_value, expected_type):
                raise ValueError(f"{actual_argument_value} is not of type: {expected_type}")

        for actual_keyword_argument_name, actual_keyword_argument_value in kwargs.items():
            expected_keyword_argument_type = type_hints[actual_keyword_argument_name]

            if not isinstance(actual_keyword_argument_value, expected_keyword_argument_type):
                raise ValueError(f"{actual_keyword_argument_value} is not of type: {expected_keyword_argument_type}")

        return_result = function(*args, **kwargs)

        expected_return_type = type_hints["return"]

        if not isinstance(return_result, expected_return_type):
            raise ValueError(f"{return_result} is not of type: {expected_return_type}")

        return return_result

    return wrapper
