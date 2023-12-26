import logging
import typing as ty
from dataclasses import dataclass

from .bind import Bind
from .exceptions import AlwaysReinitNotCallable, InterfaceNotFound
from .meta import Singleton

__all__ = ("Injktor", "Config")

logger = logging.getLogger(__name__)


@dataclass
class Config:
    binds: set[Bind]


class Injktor(metaclass=Singleton):
    _impls_cache: dict[type, ty.Any] = {}
    _binds_map: dict[type, Bind] = {}

    def __init__(self, config: Config | None = None):
        self.config = config or Config(set())
        self.install_binds(self.config.binds)
        logger.info("Injktor initialized")

    def install_binds(self, binds: set[Bind]) -> None:
        logger.debug(f"Installing {len(binds)} binds")
        for bind_conf in binds:
            self.set(bind_conf)

    def set(self, bind_conf: Bind) -> None:
        logger.debug(f"Setting {bind_conf.interface} to {bind_conf.implementation}")
        self._binds_map[bind_conf.interface] = bind_conf
        self._impls_cache.pop(bind_conf.interface, None)

    def delete(self, interface: type) -> None:
        logger.debug(f"Deleting {interface}")
        self._binds_map.pop(interface, None)
        self._impls_cache.pop(interface, None)

    def clear(self) -> None:
        logger.debug("Clearing all binds")
        self._binds_map.clear()
        self._impls_cache.clear()

    def get(self, interface: type) -> type:
        bind_conf = self._binds_map.get(interface)
        if bind_conf is None:
            raise InterfaceNotFound(interface)

        if bind_conf.always_reinit:
            logger.debug(
                f"Re-Initializing {bind_conf.implementation} as {interface} is marked always-reinit"
            )
            if not callable(bind_conf.implementation):
                raise AlwaysReinitNotCallable(bind_conf.implementation)
            return bind_conf.implementation()

        impl_cls = self._impls_cache.get(interface)
        if not impl_cls:
            logger.debug(
                f"Cache miss for implementation of {interface}, initializing..."
            )
            impl_cls = (
                bind_conf.implementation()
                if callable(bind_conf.implementation)
                else bind_conf.implementation
            )
            self._impls_cache[interface] = impl_cls
        logger.debug(f"Returning cached implementation of {interface}: {impl_cls}")
        return impl_cls
