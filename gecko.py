from functools import wraps
from typing import Callable, get_type_hints


def disable(func: Callable) -> Callable:
    """This decorator prevents the function it decorates from executing"""

    @wraps(func)
    def wrapper(*args, **kwargs):  # TODO: type annotations for args
        print(f"{func.__name__} is disabled")

    return wrapper


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
