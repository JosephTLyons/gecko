from functools import wraps


def disable(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"{func.__name__} is disabled")

    return wrapper


@disable
def get_greeting_string(name: str) -> str:
    """Gets a greeting string"""
    return f"Hello, {name}"


def main() -> None:
    print(get_greeting_string("Joseph"))


if __name__ == "__main__":
    main()
