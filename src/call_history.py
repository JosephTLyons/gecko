class CallHistoryEntry:
    def __init__(self, function_object, *args, **kwargs):
        self.function_name = function_object.__code__.co_name
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        args = [f"\"{arg}\"" if isinstance(arg, str) else arg for arg in self.args]
        kwargs = {key: f"\"{value}\"" if isinstance(value, str) else value for key, value in self.kwargs.items()}

        arg_string = ", ".join(str(arg) for arg in args)
        kwarg_string = ", ".join(f"{key}={value}" for key, value in kwargs.items())

        final_input_list = [arg_string, kwarg_string]
        final_input_string = ", ".join(final_input_list)

        return f"{self.function_name}({final_input_string})"

# Curretly, this class gets tests indirectly through the tests ran for the call_history decorator
# We might want to add some tests that run directly on this class
