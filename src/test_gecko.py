from enum import Enum, auto

from src.gecko import call_count, disable, retry
from ward import test

# Test `call_count` ================================================================================

@test("Test the call_count decorator")
def _() -> None:
    @call_count
    def decorated_function() -> None:
        pass

    count_count: int = 3

    for _ in range(count_count):
        decorated_function()

    assert decorated_function.call_count == count_count  # type: ignore

# Test `disable` ===================================================================================

@test("Test the disable decorator")
def _() -> None:
    @disable()
    def decorated_function() -> str:
        return "Hello World!"

    assert decorated_function() is None

# Test `retry` =====================================================================================

class RetryDecoratorResultType(Enum):
    SUCCESS = auto()
    FAILED_VIA_EXHAUSTING_RETRIES_ON_SPECIFIED_EXCEPTIONS = auto()
    FAILED_VIA_UNSPECIFIED_EXCEPTIONS = auto()

@test("Test the retry decorator - passing case")
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


@test("Test the retry decorator - too many exceptions fail case")
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


@test("Test the retry decorator - different exception fail case")
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
