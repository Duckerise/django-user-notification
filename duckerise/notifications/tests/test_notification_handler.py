import pytest

from ..exceptions import RelatedEventNotFound, RelatedUserNotFound
from ..handler import NotificationSender
from ..tests.helpers import NonRefObjClass, RefObjClass
from ..utils import uses_db
from .factories import NotificationEventFactory, NotificationHandlerFactory, UserFactory


@uses_db
def test_getting_user_from_ref_obj():
    user = UserFactory()
    sender1 = NotificationHandlerFactory(ref_obj=user)
    sender2 = NotificationHandlerFactory(ref_obj=RefObjClass(user))
    sender3 = NotificationHandlerFactory(ref_obj=NonRefObjClass())

    assert sender1.user == user
    assert sender2.user == user

    with pytest.raises(RelatedUserNotFound):
        sender3.user


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
