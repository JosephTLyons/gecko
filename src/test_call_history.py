from unittest.mock import call
from ward import test

from src.call_history import CallHistoryEntry


def function() -> None:
    pass


for function_object, args, kwargs, call_string in (
    (function, (), {}, "function()"),
    (function, (1, "hi"), {}, 'function(1, "hi")'),
    (function, (), {"dog": 2, "cat": 3.14}, "function(dog=2, cat=3.14)"),
    (
        function,
        (1, "hi"),
        {"dog": 2, "cat": 3.14},
        'function(1, "hi", dog=2, cat=3.14)',
    ),
):

    @test("Test `CallHistoryEntry`", tags=["call_count"])
    def _(
        function_object=function_object,
        args=args,
        kwargs=kwargs,
        call_string=call_string,
    ) -> None:
        call_history_entry: CallHistoryEntry = CallHistoryEntry(function_object, *args, **kwargs)

        assert call_history_entry.function_object == function_object
        assert call_history_entry.args == args
        assert call_history_entry.kwargs == kwargs
        assert str(call_history_entry) == call_string
