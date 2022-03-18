import time

from functools import wraps
from typing import Any, Callable, TypeVar, cast

from src.call_history import CallHistoryEntry


# https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
Func = TypeVar("Func", bound=Callable[..., Any])


def call_count(func: Func) -> Func:
    """This decorator keeps track of the number of times the function it decorates is called."""

    @wraps(func)
    def wrapper(*args, **kwargs):  # type: ignore
        wrapper.call_count += 1  # type: ignore
        return func(*args, **kwargs)

    wrapper.call_count: int = 0  # type: ignore

    return cast(Func, wrapper)


def call_history(history_length: int | None = None) -> Callable[[Func], Func]:
    def decorator(func: Func) -> Func:
        """This decorator keeps track of the call history of the function it decorates."""

        @wraps(func)
        def wrapper(*args, **kwargs):  # type: ignore
            call_history_entry: CallHistoryEntry = CallHistoryEntry(
                func, *args, **kwargs
            )
            wrapper.call_history.insert(0, call_history_entry)

            if history_length and len(wrapper.call_history) > history_length:
                wrapper.call_history.pop(-1)

            return func(*args, **kwargs)

        wrapper.call_history: list[CallHistory] = []  # type: ignore

        return cast(Func, wrapper)

    return decorator


def disable(
    should_print_details: bool = False, return_value: Any | None = None
) -> Callable[[Func], Func]:
    def decorator(func: Func) -> Func:
        """This decorator prevents the function it decorates from executing."""

        @wraps(func)
        def wrapper(*args, **kwargs):  # type: ignore
            if should_print_details:
                print(f"{func.__name__} is disabled")

            return return_value

        return cast(Func, wrapper)

    return decorator


def retry(
    *exceptions: type[BaseException],
    number_of_retries: int = 3,
    duration_between_retries_in_seconds: float = 1.0,
    should_print_details: bool = False,
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


# TODO:
# Fix mypy errors
# add TODO / Implement decorator | Implement(notes: ) -> raises TODO exception with notes
# Use ward's exception testing
# Name: MUD?
