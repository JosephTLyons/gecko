import time

from functools import wraps
from typing import Any, Callable, TypeVar, cast, get_type_hints


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
    duration_between_retries_in_seconds: float = 1.0,
    should_print_details: bool = False
) -> Callable[[Func], Func]:
    """
    This decorator re-calls the function it decorates when the function raises any of the `Exception` supplied to it via `*exceptions`.
    It should be noted that the function is called once before any retries are attempted.  Because of this,
    the maximum number of times the function can be called is `number_of_retries` + 1.
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


def validate(func: Func) -> Func:
    """
    This decorator validates the input and output data types of the function it decorates.
    It raises an `Exception` if the actual data types do not match what is provided in the hinting.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):  # type: ignore
        type_hints = get_type_hints(func)

        # Code this such that it omits things that aren't hinted

        expected_types = list(type_hints.values())

        for actual_argument_value, expected_type in zip(args, expected_types):
            if not isinstance(actual_argument_value, expected_type):
                raise ValueError(f"{actual_argument_value} is not of type: {expected_type}")

        for actual_keyword_argument_name, actual_keyword_argument_value in kwargs.items():
            expected_keyword_argument_type = type_hints[actual_keyword_argument_name]

            if not isinstance(actual_keyword_argument_value, expected_keyword_argument_type):
                raise ValueError(f"{actual_keyword_argument_value} is not of type: {expected_keyword_argument_type}")

        return_result = func(*args, **kwargs)

        expected_return_type = type_hints["return"]

        if not isinstance(return_result, expected_return_type):
            raise ValueError(f"{return_result} is not of type: {expected_return_type}")

        return return_result

    return cast(Func, wrapper)
