from src.gecko import call_count, call_history, disable, retry
from ward import raises, test

# NOTE: May not need to keep tests separated into test_ file now that we are using Ward - investigate

# Test `call_count` ================================================================================


@test("Test `call_count` decorator", tags=["call_count"])
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


@test("Test `call_history` decorator - no history purge", tags=["call_history"])
def _() -> None:
    @call_history(history_length=2)
    def decorated_function() -> None:
        pass

    decorated_function()
    decorated_function()

    assert len(decorated_function.call_history) == 2


@test("Test `call_history` decorator - history purge", tags=["call_history"])
def _() -> None:
    @call_history(history_length=1)
    def decorated_function() -> None:
        pass

    decorated_function()
    decorated_function()

    assert len(decorated_function.call_history) == 1


# Test `disable` ===================================================================================


@test("Test `disable` decorator - with a `None` return value", tags=["disable"])
def _() -> None:
    @disable()
    def decorated_function() -> str:
        return "Hello World!"

    assert decorated_function() is None


@test("Test `disable` decorator - with a user-specified return value", tags=["disable"])
def _() -> None:
    @disable(return_value=0)
    def decorated_function(number_1: int, number_2: int) -> int:
        return number_1 + number_2

    assert decorated_function(1, 2) == 0


# Test `retry` =====================================================================================


@test(
    "Test `retry` decorator - the number of retries is equal to the number of exceptions raised",
    tags=["retry"],
)
def _() -> None:
    number_of_exceptions = 3
    exceptions_to_raise: list[type[BaseException]] = [FileExistsError] * number_of_exceptions
    exceptions_to_catch: tuple[type[BaseException], ...] = tuple(exceptions_to_raise)

    @retry(
        *exceptions_to_catch,
        number_of_retries=number_of_exceptions,
        duration_between_retries_in_seconds=0.01
    )
    def decorated_function() -> None:
        if exceptions_to_raise:
            raise exceptions_to_raise.pop(0)

    decorated_function()


@test(
    "Test `retry` decorator - the number of retries is less than the number of exceptions raised",
    tags=["retry"],
)
def _() -> None:
    exception_to_raise = FileExistsError
    number_of_exceptions = 4
    exceptions_to_raise: list[type[BaseException]] = [exception_to_raise] * number_of_exceptions
    exceptions_to_catch: tuple[type[BaseException], ...] = tuple(exceptions_to_raise)

    @retry(
        *exceptions_to_catch,
        number_of_retries=number_of_exceptions - 1,
        duration_between_retries_in_seconds=0.01
    )
    def decorated_function() -> None:
        if exceptions_to_raise:
            raise exceptions_to_raise.pop(0)

    with raises(exception_to_raise):
        decorated_function()


@test(
    "Test `retry` decorator - the decorated function should raise any Exception that it is not asked to catch",
    tags=["retry"],
)
def _() -> None:
    exception_to_raise = ZeroDivisionError

    @retry(OSError, number_of_retries=1, duration_between_retries_in_seconds=0.01)
    def decorated_function() -> None:
        raise exception_to_raise

    with raises(exception_to_raise):
        decorated_function()
