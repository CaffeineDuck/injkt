# Injkt (Dependency ~~injection~~ injktion)

Your simple python DI library built with good intentions.

## Install

```shell
pip install injkt
```

## Why?

Good question.

## How?

```python
import typing as ty

from injkt import Bind, Config, Injectable, Injktor, inject_args_deps


class IMailService(ty.Protocol):
    def send_mail(self, subject: str, to: str) -> None:
        ...


class SmtpMailService(IMailService):
    def send_mail(self, subject: str, to: str) -> None:
        raise NotImplementedError()


injktor = Injktor(
    Config(
        {
            Bind(IMailService, SmtpMailService),
        }
    )
)


@inject_args_deps
def business_logic(mail_service=Injectable(IMailService)):
    mail_service.send_mail("Hello", "world")


business_logic()
```

### Class Based

```python
from injktor import inject_attr_deps

@inject_attr_deps
class BusinessLogic:
    mail_service = Injectable(IMailService)

    def do_business_logic(self) -> None:
        self.mail_service.send_mail("Hello", "world")


BusinessLogic().do_business_logic()
```

### Class based lazy injection

```python
from injktor import InjktLazy

class BusinessLogic(InjktLazy):
    mail_service = Injectable(IMailService)

    def do_business_logic(self) -> None:
        self.mail_service.send_mail("Hello", "world")


BusinessLogic().do_business_logic()
```

### Re-init dependencies

```python
injktor = Injktor(
    Config(
        {
            Bind(IMailService, SmtpMailService, always_reinit=True),
        }
    )
)
```

Enabling `always_reinit` will re-initialize the dependency on each call.
**NOTE: It won't be re-initialized in the same class if you aren't using `InjktLazy`**
