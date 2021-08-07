from gecko import disable


def test_disable_decorator() -> None:
    @disable
    def decorated_function() -> str:
        return "Hello World!"

    assert(decorated_function() is None)
