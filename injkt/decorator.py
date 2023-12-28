import inspect
import typing as ty
from functools import wraps

from .injectable import Injectable
from .injktor import Injktor

__all__ = ("inject_attr_deps", "inject_args_deps")

def inject_attr_deps[T](cls_: T) -> T:
    injktor = Injktor()
    for attr_name in dir(cls_):
        attr = getattr(cls_, attr_name)
        if not isinstance(attr, Injectable):
            continue
        impl_cls = injktor.get(attr.__injection__)
        setattr(cls_, attr_name, impl_cls)
    return cls_


def inject_args_deps[T, **P](func: ty.Callable[P, T]) -> ty.Callable[P, T]:
    @wraps(func)
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        sig = inspect.signature(func)
        defaults = {
            name: param.default
            for name, param in sig.parameters.items()
            if param.default is not inspect.Parameter.empty
        }

        for arg_name, arg in defaults.items():
            if not isinstance(arg, Injectable):
                continue
            impl_cls = Injktor().get(arg.__injection__)
            kwargs[arg_name] = impl_cls

        return func(*args, **kwargs)

    return wrapper
