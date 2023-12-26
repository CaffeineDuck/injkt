__all__ = (
    "DIConfigurationError",
    "InterfaceNotFound",
    "AlwaysReinitNotCallable",
)


class DIConfigurationError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "DI not configured properly, Injectable not replaced with dependency."
        )


class InterfaceNotFound(Exception):
    def __init__(self, interface: type) -> None:
        self.interface = interface
        super().__init__(f"Interface {interface} not found.")


class AlwaysReinitNotCallable(TypeError):
    def __init__(self, implementation: type) -> None:
        self.implementation = implementation
        super().__init__(f"Implementation {implementation} is not callable.")
