from notifications.tests.factories import UserFactory

from ..handler import NotificationHandler
from ..utils import uses_db


@uses_db
def test_notification_handler_init():
    user = UserFactory()
    sender = NotificationHandler(user, None)
    text = (
        "My name is {{ username }}. "
        "My email is {{email}}. "
        "And my name is {{       first_name  }}"
    )
    correct_text = (
        f"My name is {user.username}. "
        f"My email is {user.email}. "
        f"And my name is {user.first_name}"
    )

    assert sender.replace_variables(text) == correct_text
