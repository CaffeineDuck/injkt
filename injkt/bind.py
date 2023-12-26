import typing as ty
from dataclasses import dataclass

__all__ = ("Bind",)


@dataclass
class Bind:
    interface: type
    implementation: type | ty.Callable[[], ty.Any]
    always_reinit: bool = False

    def __hash__(self) -> int:
        return hash(self.interface)

    def __eq__(self, other: ty.Any) -> bool:
        if not isinstance(other, Bind):
            return False
        return self.interface == other.interface
