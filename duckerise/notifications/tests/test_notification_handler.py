import pytest

from ..exceptions import RelatedUserNotFound
from ..handler import NotificationHandler, NotificationSender
from ..tests.helpers import NonRefObjClass, RefObjClass
from ..utils import uses_db
from .factories import NotificationEventFactory, UserFactory


@uses_db
def test_getting_user_from_ref_obj():
    user = UserFactory()
    sender1 = NotificationHandler(user, None)
    sender2 = NotificationHandler(RefObjClass(user), None)
    sender3 = NotificationHandler(NonRefObjClass(), None)

    assert sender1.user == user
    assert sender2.user == user

    with pytest.raises(RelatedUserNotFound):
        sender3.user


@uses_db
def test_getting_notification():
    notification_event = NotificationEventFactory()
    notification_event.label


@uses_db
def test_notification_handler_init():
    user = UserFactory()
    sender = NotificationHandler(user, None)
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
    print(correct_text)
    assert sender.replace_variables(text) == correct_text


def test_getting_list_of_sender_subclassses():
    class SMSSender(NotificationSender):
        pass

    class EmailSender(NotificationSender):
        pass

    subclasses_dict = {
        SMSSender.__name__: SMSSender,
        EmailSender.__name__: EmailSender,
    }

    assert NotificationHandler(None, None).all_senders == subclasses_dict