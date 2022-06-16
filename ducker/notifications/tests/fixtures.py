import pytest

from ..handler import NotificationSender


class NonInheretedClass:
    pass


# After finishing our job with classes, we change
# the base (inherited) of these classes, to "break"
# link between these and NotificationSender class
# which updates `__subclasses__` function
# https://stackoverflow.com/a/52442961/8842262
@pytest.fixture
def no_slug_sms_sender_class():
    class SMSSender(NotificationSender):
        pass

    yield SMSSender
    SMSSender.__bases__ = (NonInheretedClass,)


@pytest.fixture
def sms_sender_class():
    class SMSSender(NotificationSender):
        SLUG = "sms"

        def send(self, user, text):
            pass

    yield SMSSender
    SMSSender.__bases__ = (NonInheretedClass,)


@pytest.fixture
def email_sender_class():
    class EmailSender(NotificationSender):
        SLUG = "email"

        def send(self, user, text):
            pass

    yield EmailSender
    EmailSender.__bases__ = (NonInheretedClass,)
