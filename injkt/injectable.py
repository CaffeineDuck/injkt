import typing as ty

from .exceptions import DIConfigurationError

__all__ = ("Injectable",)

T = ty.TypeVar("T")


class Injectable(ty.Generic[T]):
    __injection__: type

    def __new__(cls, injection_class: type[T]) -> T:
        if injection_class == Injectable:
            raise ValueError("Injectable cannot be injected.")

        self = super().__new__(cls)
        self.__injection__ = injection_class
        return self  # type: ignore

    def __getattr__(self, _: str) -> None:
        raise DIConfigurationError()
