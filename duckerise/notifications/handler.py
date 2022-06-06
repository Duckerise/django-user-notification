import sys
from typing import Optional

from django.contrib.auth import get_user_model
from django.db.models import Model

from notifications.utils import QuerySetType

from .exceptions import RelatedEventNotFound
from .models import NotificationEvent

if sys.version_info >= (3, 3):
    from collections.abc import Iterable
else:
    from collections import Iterable


UserModel: Model = get_user_model()


class NotificationHandler:
    pass


class NotificationSender:
    def __init__(self, ref_obj: Model, identifier: str) -> None:
        self.ref_obj = ref_obj
        self.identifier = identifier

    def get_user(self) -> UserModel:
        pass

    def get_notification(self) -> Optional[NotificationEvent]:
        return (
            NotificationEvent.objects.filter(identifier=self.identifier)
            .prefetch_related("mediums")
            .first()
        )

    def replace_variables(self, text: str) -> str:
        replaced_text = text
        regex = r"(?<={{)(w+)(?=}})"

        return replaced_text

    def get_sender(self):
        pass

    def get_sender_function(self):
        pass

    def send(self) -> None:
        notification = self.get_notification()

        if not notification:
            raise RelatedEventNotFound(
                "No event found with identifier %s".format(self.identifier)
            )

        for medium in notification.mediums:
            raw_text = notification.get_text_for_medium(medium)
            text = self.replace_variables(raw_text)
            sender_function = self.get_sender_function()
            sender_function(self.get_user(), text)
