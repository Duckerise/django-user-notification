from unittest import mock

import pytest

from ..exceptions import (
    RelatedEventNotFound,
    RelatedSenderClassNotFound,
    RelatedUserNotFound,
)
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


# So that, inner classes do not affect further tests
# we reduce test unit scope
@pytest.fixture(scope="function")
def test_getting_list_of_sender_subclassses():
    class SMSSender(NotificationSender):
        SLUG = "sms"

    class EmailSender(NotificationSender):
        SLUG = "email"

    subclasses_dict = {
        SMSSender.SLUG: SMSSender,
        EmailSender.SLUG: EmailSender,
    }

    assert NotificationHandlerFactory().all_senders == subclasses_dict


@uses_db
@pytest.fixture(scope="function")
def test_getting_sender_with_slug():
    class SMSSender(NotificationSender):
        SLUG = "sms"

    class EmailSender(NotificationSender):
        SLUG = "email"

    medium = MediumFactory(slug="email")

    assert isinstance(NotificationHandlerFactory().get_sender(medium), EmailSender)


@uses_db
@pytest.fixture(scope="function")
def test_getting_sender_without_slug():
    class SMSSender(NotificationSender):
        pass

    medium = MediumFactory(slug="sms")

    with pytest.raises(RelatedSenderClassNotFound):
        NotificationHandlerFactory().get_sender(medium)


@uses_db
@pytest.fixture(scope="function")
def test_getting_sender_function():
    class SMSSender(NotificationSender):
        SLUG = "SMS"

        def send(self):
            pass

    medium = MediumFactory(slug="SMS")
    handler = NotificationHandlerFactory()

    # Make sure the function belongs to SMSSender class
    assert handler.get_sender_function(medium).__self__.__class__ == SMSSender


@uses_db
@pytest.fixture(scope="function")
def test_whole_logic():
    class SMSSender(NotificationSender):
        SLUG = "sms"

        def send(self, *args, **kwargs):
            pass

    class EmailSender(NotificationSender):
        SLUG = "email"

        def send(self, *args, **kwargs):
            pass

    user = UserFactory()
    identifier = "auth__user"
    mediums = [MediumFactory(slug="sms"), MediumFactory(slug="email")]
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
