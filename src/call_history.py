class CallHistoryEntry:
    def __init__(self, function_object, *args, **kwargs):  # type: ignore
        self.function_object = function_object
        self.args = args
        self.kwargs = kwargs

    def __str__(self) -> str:
        function_name: str = self.function_object.__name__

        args = [f'"{arg}"' if isinstance(arg, str) else arg for arg in self.args]
        kwargs = {
            key: f'"{value}"' if isinstance(value, str) else value
            for key, value in self.kwargs.items()
        }

        final_input_list: list[str] = []

        arg_string: str = ", ".join(str(arg) for arg in args)

        if arg_string:
            final_input_list.append(arg_string)

        kwarg_string: str = ", ".join(f"{key}={value}" for key, value in kwargs.items())

        if kwarg_string:
            final_input_list.append(kwarg_string)

        final_input_string: str = ", ".join(final_input_list)

        return f"{function_name}({final_input_string})"
