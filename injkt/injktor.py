import logging
import typing as ty
from dataclasses import dataclass
from functools import cached_property

from .bind import Bind
from .exceptions import AlwaysReinitNotCallable, InterfaceNotFound
from .meta import Singleton

__all__ = ("Injktor", "InjktorConfig")

logger = logging.getLogger(__name__)


@dataclass
class InjktorConfig:
    binds: set[Bind]


class Injktor(metaclass=Singleton):
    _impls_cache: dict[type, ty.Any] = {}

    def __init__(self, config: InjktorConfig | None = None):
        logger.info("Initializing Injktor")
        self.config = config or InjktorConfig(set())
        logger.info("Injktor initialized")

    @cached_property
    def _binds_map(self) -> dict[type, Bind]:
        return {bind.interface: bind for bind in self.config.binds}

    def set(self, bind_conf: Bind) -> None:
        self.config.binds.add(bind_conf)

    def get(self, interface: type) -> type:
        bind_conf = self._binds_map.get(interface)
        if bind_conf is None:
            raise InterfaceNotFound(interface)

        if bind_conf.always_reinit:
            if not callable(bind_conf.implementation):
                raise AlwaysReinitNotCallable(bind_conf.implementation)
            return bind_conf.implementation()

        impl_cls = self._impls_cache.get(interface)
        if not impl_cls:
            impl_cls = bind_conf.implementation()
            self._impls_cache[interface] = impl_cls
        return impl_cls
