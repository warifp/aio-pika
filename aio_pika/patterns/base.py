import pickle
from typing import Any, Callable


class Method:
    __slots__ = (
        "name",
        "func",
    )

    def __init__(self, name: str, func: Callable[..., Any]):
        self.name = name
        self.func = func

    def __getattr__(self, item: str) -> "Method":
        return Method(".".join((self.name, item)), func=self.func)

    def __call__(self, **kwargs: Any) -> Any:
        return self.func(self.name, kwargs=kwargs)


class Proxy:
    __slots__ = ("func",)

    def __init__(self, func: Callable[..., Any]):
        self.func = func

    def __getattr__(self, item: str) -> Method:
        return Method(item, self.func)


class Base:
    SERIALIZER = pickle
    CONTENT_TYPE = "application/python-pickle"

    def serialize(self, data: Any) -> bytes:
        return self.SERIALIZER.dumps(data)

    def deserialize(self, data: bytes) -> Any:
        return self.SERIALIZER.loads(data)
