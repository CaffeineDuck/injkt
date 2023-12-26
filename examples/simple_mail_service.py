from abc import ABC, abstractmethod

from injkt import Bind, Config, Injectable, Injktor, inject_args_deps


class IMailService(ABC):
    @abstractmethod
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
