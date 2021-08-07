from gecko import disable, retry


def test_disable_decorator() -> None:
    @disable
    def decorated_function() -> str:
        return "Hello World!"

    assert(decorated_function() is None)


def test_retry_decorator_pass() -> None:
    # We want the `decorated_function` to raise 3 exceptions.  The number of times the function will be called is `number_of_retries` + 1
    # Thus, we have 3 raises and 4 calls to the function, so the function will not raise on the final call and the test should
    # pass only if the test is ran without catching any exceptions from the `decorated_function`.
    __test_retry_decorator_base(number_of_exceptions_raised=3, number_of_retries=3, should_catch_exception=False)


def test_retry_decorator_fail() -> None:
    # We want the `decorated_function` to raise 4 exceptions.  The number of times the function will be called is `number_of_retries` + 1
    # Thus, we have 4 raises and 4 calls to the function, so the function will raise on the final call and the test should
    # pass only if the test is catches an exception raised by the `decorated_function`.
    __test_retry_decorator_base(number_of_exceptions_raised=4, number_of_retries=3, should_catch_exception=True)


def __test_retry_decorator_base(number_of_exceptions_raised, number_of_retries, should_catch_exception) -> None:
    # Used to simimulate a function raising multiple exceptions
    exceptions = [FileNotFoundError] * number_of_exceptions_raised

    @retry((FileNotFoundError,), number_of_retries, 0.01)
    def decorated_function() -> None:
        if exceptions:
            raise exceptions.pop()

        return None

    try:
        decorated_function()
        assert(not should_catch_exception)
    except FileNotFoundError:
        assert(should_catch_exception)
