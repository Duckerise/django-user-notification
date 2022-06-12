from unittest import mock

import pytest

from ..exceptions import RelatedEventNotFound, RelatedUserNotFound
from ..handler import NotificationSender
from ..tests.helpers import NonRefObjClass, RefObjClass
from ..utils import uses_db
from .factories import (
    MediumFactory,
    NotificationEventFactory,
    NotificationHandlerFactory,
    UserFactory,
)


@uses_db
def test_getting_user_from_ref_obj():
    user = UserFactory()
    handler1 = NotificationHandlerFactory(ref_obj=user)
    handler2 = NotificationHandlerFactory(ref_obj=RefObjClass(user))
    handler3 = NotificationHandlerFactory(ref_obj=NonRefObjClass())

    assert handler1.user == user
    assert handler2.user == user

    with pytest.raises(RelatedUserNotFound):
        handler3.user


@uses_db
def test_getting_notification():
    identifier = "auth__user"
    notification_event = NotificationEventFactory(identifier=identifier)

    assert NotificationHandlerFactory(identifier=identifier).event == notification_event

    with pytest.raises(RelatedEventNotFound):
        assert NotificationHandlerFactory(identifier="random_identifier").event


@uses_db
def test_notification_handler_init():
    user = UserFactory()
    text = (
        "My nickname is {{ username }}. "
        "My email is {{email}}. "
        "And my name is {{       first_name  }}"
    )
    correct_text = (
        f"My nickname is {user.username}. "
        f"My email is {user.email}. "
        f"And my name is {user.first_name}"
    )
    assert (
        NotificationHandlerFactory(ref_obj=user).replace_variables(text) == correct_text
    )


def test_getting_list_of_sender_subclassses():
    class SMSSender(NotificationSender):
        pass

    class EmailSender(NotificationSender):
        pass

    subclasses_dict = {
        SMSSender.__name__: SMSSender,
        EmailSender.__name__: EmailSender,
    }

    assert NotificationHandlerFactory().all_senders == subclasses_dict


@uses_db
def test_getting_sender():
    class SMSSender(NotificationSender):
        pass

    class EmailSender(NotificationSender):
        pass

    medium = MediumFactory(slug="Email")

    assert isinstance(NotificationHandlerFactory().get_sender(medium), EmailSender)


@uses_db
def test_getting_sender_function():
    class SMSSender(NotificationSender):
        def send(self):
            pass

    medium = MediumFactory(slug="SMS")
    handler = NotificationHandlerFactory()

    # Make sure the function belongs to SMSSender class
    assert handler.get_sender_function(medium).__self__.__class__ == SMSSender


@uses_db
def test_whole_logic():
    class SMSSender(NotificationSender):
        def send(self, *args, **kwargs):
            pass

    class EmailSender(NotificationSender):
        def send(self, *args, **kwargs):
            pass

    user = UserFactory()
    identifier = "auth__user"
    mediums = [MediumFactory(slug="SMS"), MediumFactory(slug="Email")]
    notification_event = NotificationEventFactory(
        identifier=identifier,
        mediums=mediums,
    )

    handler = NotificationHandlerFactory(ref_obj=user, identifier=identifier)

    with mock.patch.object(SMSSender, "send") as sms_func, mock.patch.object(
        EmailSender, "send"
    ) as email_func:
        handler.send()
        sms_func.assert_called_once_with(user, notification_event.raw_text)
        email_func.assert_called_once_with(user, notification_event.raw_text)
