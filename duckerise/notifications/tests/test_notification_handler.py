import pytest
from notifications.tests.factories import UserFactory

from ..handler import NotificationSender
from ..utils import uses_db


@uses_db
def test_notification_handler_init():
    user = UserFactory()
    sender = NotificationSender(user, None)
    text = "My name is {{ username }}. My email is {{email}}."
    correct_text = f"My name is {user.first_name}. My email is {user.email}."

    assert sender.replace_variables(text) == correct_text
