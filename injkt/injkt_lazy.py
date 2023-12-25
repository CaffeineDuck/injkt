import typing as ty

from .injectable import Injectable
from .injktor import Injktor

__all__ = ("InjktLazy",)


class InjktLazy:
    def __getattribute__(self, __name: str) -> ty.Any:
        attr = super().__getattribute__(__name)
        if not isinstance(attr, Injectable):
            return attr

        impl_cls = Injktor().get(attr.__injection__)
        return impl_cls
