from unittest import mock

import pytest

from ..exceptions import (
    RelatedEventNotFound,
    RelatedSenderClassNotFound,
    RelatedUserNotFound,
)
from ..handler import SenderType
from ..tests.helpers import NonRefObjClass, RefObjClass
from ..utils import uses_db
from .factories import (
    MediumFactory,
    NotificationEventFactory,
    NotificationHandlerFactory,
    UserFactory,
)
from .fixtures import email_sender_class, no_slug_sms_sender_class, sms_sender_class


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


def test_getting_list_of_sender_subclassses(
    email_sender_class: SenderType,
    sms_sender_class: SenderType,
):
    subclasses_dict = {
        email_sender_class.SLUG: email_sender_class,
        sms_sender_class.SLUG: sms_sender_class,
    }

    assert NotificationHandlerFactory().all_senders == subclasses_dict


@uses_db
def test_getting_sender_with_slug(email_sender_class, sms_sender_class):

    medium = MediumFactory(slug="email")
    assert isinstance(
        NotificationHandlerFactory().get_sender(medium), email_sender_class
    )


@uses_db
def test_getting_sender_without_slug(no_slug_sms_sender_class):

    medium = MediumFactory(slug="sms")

    with pytest.raises(RelatedSenderClassNotFound):
        NotificationHandlerFactory().get_sender(medium)


@uses_db
def test_getting_sender_function(sms_sender_class):

    medium = MediumFactory(slug="sms")
    handler = NotificationHandlerFactory()

    # Make sure the function belongs to SMSSender class
    assert handler.get_sender_function(medium).__self__.__class__ == sms_sender_class


@uses_db
def test_whole_logic(email_sender_class, sms_sender_class):

    user = UserFactory()
    identifier = "auth__user"
    mediums = [MediumFactory(slug="sms"), MediumFactory(slug="email")]
    notification_event = NotificationEventFactory(
        identifier=identifier,
        mediums=mediums,
    )

    handler = NotificationHandlerFactory(ref_obj=user, identifier=identifier)

    with mock.patch.object(sms_sender_class, "send") as sms_func, mock.patch.object(
        email_sender_class, "send"
    ) as email_func:
        handler.send()
        sms_func.assert_called_once_with(user, notification_event.raw_text)
        email_func.assert_called_once_with(user, notification_event.raw_text)
