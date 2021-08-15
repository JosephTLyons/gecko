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
    __test_retry_decorator_base(number_of_exceptions_raised=3, number_of_retries=3, try_should_succeed=True)


def test_retry_decorator_fail() -> None:
    # We want the `decorated_function` to raise 4 exceptions.  The number of times the function will be called is `number_of_retries` + 1
    # Thus, we have 4 raises and 4 calls to the function, so the function will raise on the final call and the test should
    # pass only if the test is catches an exception raised by the `decorated_function`.
    __test_retry_decorator_base(number_of_exceptions_raised=4, number_of_retries=3, try_should_succeed=False)


def __test_retry_decorator_base(number_of_exceptions_raised: int, number_of_retries: int, try_should_succeed: bool) -> None:
    # Used to simimulate a function raising multiple exceptions
    exceptions: list[type[BaseException]] = [FileNotFoundError] * number_of_exceptions_raised

    @retry(FileNotFoundError, number_of_retries=number_of_retries, duration_between_retries_in_seconds=0.01)
    def decorated_function() -> None:
        if exceptions:
            raise exceptions.pop(0)

    try:
        decorated_function()
        assert(try_should_succeed)
    except FileNotFoundError:
        assert(not try_should_succeed)
