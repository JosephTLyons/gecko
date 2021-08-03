from gecko import disable


def test_disable_decorator() -> None:
    @disable
    def hello_world() -> str:
        return "Hello World!"

    assert(hello_world() is None)
