from enum import Enum, auto

from src.gecko import disable, retry


def test_disable_decorator() -> None:
    @disable()
    def decorated_function() -> str:
        return "Hello World!"

    assert(decorated_function() is None)


class RetryDecoratorTestResultType(Enum):
    SUCCESS = auto()
    SPECIFIED_EXCEPTION = auto()
    UNSPECIFIED_EXCEPTION = auto()


def test_retry_decorator_pass() -> None:
    # We want the `decorated_function` to raise 3 exceptions.  The number of times the function will be called is `number_of_retries` + 1
    # Thus, we have 3 raises and 4 calls to the function, so the function will not raise on the final call and the test should
    # pass only if the test is ran without catching any exceptions from the `decorated_function`.

    exceptions_to_raise: list[type[BaseException]] = [FileExistsError] * 3
    exceptions_to_catch: tuple[type[BaseException], ...] = tuple(exceptions_to_raise)

    retry_decorator_test_result_type: RetryDecoratorTestResultType = __test_retry_decorator(
        exceptions_to_raise=exceptions_to_raise,
        exceptions_to_catch=exceptions_to_catch,
        number_of_retries=3,
    )

    assert(retry_decorator_test_result_type == RetryDecoratorTestResultType.SUCCESS)


def test_retry_decorator_too_many_exceptions_fail() -> None:
    # We want the `decorated_function` to raise 4 exceptions.  The number of times the function will be called is `number_of_retries` + 1
    # Thus, we have 4 raises and 4 calls to the function, so the function will raise on the final call and the test should
    # pass only if the test is catches an exception raised by the `decorated_function`.

    exceptions_to_raise: list[type[BaseException]] = [FileExistsError] * 4
    exceptions_to_catch: tuple[type[BaseException], ...] = tuple(exceptions_to_raise)

    retry_decorator_test_result_type: RetryDecoratorTestResultType = __test_retry_decorator(
        exceptions_to_raise=exceptions_to_raise,
        exceptions_to_catch=exceptions_to_catch,
        number_of_retries=3,
    )

    assert(retry_decorator_test_result_type == RetryDecoratorTestResultType.SPECIFIED_EXCEPTION)


def test_retry_decorator_different_exception_fail() -> None:
    # This test covers the case of an exception being raised by the decorated function that is not specified in the `retry` decorator.

    exceptions_to_raise: list[type[BaseException]] = [FileExistsError]
    exceptions_to_catch: tuple[type[BaseException], ...] = (FileNotFoundError,)

    retry_decorator_test_result_type: RetryDecoratorTestResultType = __test_retry_decorator(
        exceptions_to_raise=exceptions_to_raise,
        exceptions_to_catch=exceptions_to_catch,
        number_of_retries=1,
    )

    assert(retry_decorator_test_result_type == RetryDecoratorTestResultType.UNSPECIFIED_EXCEPTION)


def __test_retry_decorator(
    exceptions_to_raise: list[type[BaseException]],
    exceptions_to_catch: tuple[type[BaseException], ...],
    number_of_retries: int,
) -> RetryDecoratorTestResultType:
    """
    This is a universal testing function for the `retry` decorator.  Other functions test specific cases by calling this function.

    exceptions_to_raise -- Used to simimulate a function raising a limited amount of exceptions.  This must be a list so we can pop off raised exceptions
    exceptions_to_catch -- Used to define what the try-except should catch.  This must be a tuple to avoid the following error:
        `TypeError: exceptions must be old-style classes or derived from BaseException, not tuple`
    """

    @retry(*exceptions_to_catch, number_of_retries=number_of_retries, duration_between_retries_in_seconds=0.01)
    def decorated_function() -> None:
        if exceptions_to_raise:
            raise exceptions_to_raise.pop(0)

    try:
        decorated_function()
        return RetryDecoratorTestResultType.SUCCESS
    except exceptions_to_catch:
        return RetryDecoratorTestResultType.SPECIFIED_EXCEPTION
    except Exception:
        return RetryDecoratorTestResultType.UNSPECIFIED_EXCEPTION
