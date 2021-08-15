from copy import deepcopy

from src.gecko import disable, retry


def test_disable_decorator() -> None:
    @disable()
    def decorated_function() -> str:
        return "Hello World!"

    assert(decorated_function() is None)


def test_retry_decorator_pass() -> None:
    # We want the `decorated_function` to raise 3 exceptions.  The number of times the function will be called is `number_of_retries` + 1
    # Thus, we have 3 raises and 4 calls to the function, so the function will not raise on the final call and the test should
    # pass only if the test is ran without catching any exceptions from the `decorated_function`.

    exceptions_to_raise: list[type[BaseException]] = [FileExistsError] * 3
    exceptions_to_catch: tuple[type[BaseException], ...] = tuple(exceptions_to_raise)

    __test_retry_decorator(
        exceptions_to_raise=exceptions_to_raise,
        exceptions_to_catch=exceptions_to_catch,
        number_of_retries=3,
        try_should_succeed=True
    )


def test_retry_decorator_fail() -> None:
    # We want the `decorated_function` to raise 4 exceptions.  The number of times the function will be called is `number_of_retries` + 1
    # Thus, we have 4 raises and 4 calls to the function, so the function will raise on the final call and the test should
    # pass only if the test is catches an exception raised by the `decorated_function`.

    exceptions_to_raise: list[type[BaseException]] = [FileExistsError] * 4
    exceptions_to_catch: tuple[type[BaseException], ...] = tuple(exceptions_to_raise)

    __test_retry_decorator(
        exceptions_to_raise=exceptions_to_raise,
        exceptions_to_catch=exceptions_to_catch,
        number_of_retries=3,
        try_should_succeed=False
    )


def __test_retry_decorator(
    exceptions_to_raise: list[type[BaseException]],
    exceptions_to_catch: tuple[type[BaseException], ...],
    number_of_retries: int,
    try_should_succeed: bool
) -> None:
    """
    This is a universal testing function for the `retry` decorator.  Other functions test specific cases by calling this function.

    exceptions_to_raise -- Used to simimulate a function raising a limited amount of exceptions.  This must be a list so we can pop off raised exceptions
    exceptions_to_catch -- Used to define what the try-except should catch.  This must be a tuple to avoid the following error:
        `TypeError: exceptions must be old-style classes or derived from BaseException, not tuple`
    """

    @retry(*exceptions_to_raise, number_of_retries=number_of_retries, duration_between_retries_in_seconds=0.01)
    def decorated_function() -> None:
        if exceptions_to_raise:
            raise exceptions_to_raise.pop(0)

    try:
        decorated_function()
        assert(try_should_succeed)
    except exceptions_to_catch:
        assert(not try_should_succeed)
