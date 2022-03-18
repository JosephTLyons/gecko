from enum import Enum, auto

from src.gecko import call_count, call_history, disable, retry
from ward import test

# NOTE: May not need to keep tests separated into test_ file now that we are using Ward - investigate

# Test `call_count` ================================================================================

@test("Test call_count decorator")
def _() -> None:
    @call_count
    def decorated_function() -> None:
        pass

    count_count: int = 3

    for _ in range(count_count):
        decorated_function()

    assert decorated_function.call_count == count_count  # type: ignore

# Test `call_history` ==============================================================================

# We will want better testing for this decorator.  The only test here has many asserts and tests a bunch of variations at once
# This should be split up into multiple tests at some point

@test("Test call_history decorator")
def _() -> None:
    @call_history(history_length=1)
    def decorated_function(num: int, text: str, dog: int = 1, cat: float = 0.1) -> None:
        pass

    args = 1, "hi"
    kwargs = {"dog": 2, "cat": 3.14}

    decorated_function(*args, **kwargs)
    decorated_function(*args, **kwargs)

    assert len(decorated_function.call_history) == 1

    call_history_entry = decorated_function.call_history[0]

    assert call_history_entry.args == args
    assert call_history_entry.kwargs == kwargs
    assert str(call_history_entry) == "decorated_function(1, \"hi\", dog=2, cat=3.14)"

# Test `disable` ===================================================================================

@test("Test disable decorator - with a `None` return value")
def _() -> None:
    @disable()
    def decorated_function() -> str:
        return "Hello World!"

    assert decorated_function() is None


@test("Test disable decorator - with a user-specified return value")
def _() -> None:
    @disable(return_value=0)
    def decorated_function(number_1: int, number_2: int) -> int:
        return number_1 + number_2

    assert decorated_function(1, 2) == 0

# Test `retry` =====================================================================================

class RetryDecoratorResultType(Enum):
    SUCCESS = auto()
    FAILED_VIA_EXHAUSTING_RETRIES_ON_SPECIFIED_EXCEPTIONS = auto()
    FAILED_VIA_UNSPECIFIED_EXCEPTIONS = auto()

@test("Test retry decorator - passing case")
def _() -> None:
    # This test covers the case of the decorated function raising less exceptions than the retry decorator is defined to catch.
    # It should be noted that the decorated function is raising exceptions that the decorator is defined to retry on.

    exceptions_to_raise: list[type[BaseException]] = [FileExistsError] * 3
    exceptions_to_catch: tuple[type[BaseException], ...] = tuple(exceptions_to_raise)

    retry_decorator_test_result_type: RetryDecoratorResultType = __test_retry_decorator(
        exceptions_to_raise=exceptions_to_raise,
        exceptions_to_catch=exceptions_to_catch,
        number_of_retries=3,
    )

    assert retry_decorator_test_result_type == RetryDecoratorResultType.SUCCESS


@test("Test retry decorator - too many exceptions fail case")
def _() -> None:
    # This test covers the case of the decorated function raising more exceptions than the retry decorator is defined to catch.
    # It should be noted that the decorated function is raising exceptions that the decorator is definied to retry on

    exceptions_to_raise: list[type[BaseException]] = [FileExistsError] * 4
    exceptions_to_catch: tuple[type[BaseException], ...] = tuple(exceptions_to_raise)

    retry_decorator_test_result_type: RetryDecoratorResultType = __test_retry_decorator(
        exceptions_to_raise=exceptions_to_raise,
        exceptions_to_catch=exceptions_to_catch,
        number_of_retries=3,
    )

    assert retry_decorator_test_result_type == RetryDecoratorResultType.FAILED_VIA_EXHAUSTING_RETRIES_ON_SPECIFIED_EXCEPTIONS


@test("Test retry decorator - different exception fail case")
def _() -> None:
    # This test covers the case of an exception being raised by the decorated function that is not specified in the `retry` decorator.

    exceptions_to_raise: list[type[BaseException]] = [FileExistsError]
    exceptions_to_catch: tuple[type[BaseException], ...] = (FileNotFoundError,)

    retry_decorator_test_result_type: RetryDecoratorResultType = __test_retry_decorator(
        exceptions_to_raise=exceptions_to_raise,
        exceptions_to_catch=exceptions_to_catch,
        number_of_retries=1,
    )

    assert retry_decorator_test_result_type == RetryDecoratorResultType.FAILED_VIA_UNSPECIFIED_EXCEPTIONS


def __test_retry_decorator(
    exceptions_to_raise: list[type[BaseException]],
    exceptions_to_catch: tuple[type[BaseException], ...],
    number_of_retries: int,
) -> RetryDecoratorResultType:
    """
    This is a universal testing function for the `retry` decorator.  Other functions test specific cases by calling this function.

    exceptions_to_raise -- Used to simulate a function raising a limited amount of exceptions.  This must be a list so we can pop off raised exceptions
    exceptions_to_catch -- Used to define what the try-except should catch.  This must be a tuple to avoid the following error:
        `TypeError: exceptions must be old-style classes or derived from BaseException, not tuple`
    """

    @retry(*exceptions_to_catch, number_of_retries=number_of_retries, duration_between_retries_in_seconds=0.01)
    def decorated_function() -> None:
        if exceptions_to_raise:
            raise exceptions_to_raise.pop(0)

    try:
        decorated_function()
        return RetryDecoratorResultType.SUCCESS
    except exceptions_to_catch:
        return RetryDecoratorResultType.FAILED_VIA_EXHAUSTING_RETRIES_ON_SPECIFIED_EXCEPTIONS
    except Exception:
        return RetryDecoratorResultType.FAILED_VIA_UNSPECIFIED_EXCEPTIONS
