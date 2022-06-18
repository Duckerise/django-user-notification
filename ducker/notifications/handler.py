import logging
import re
import sys
from functools import cached_property
from typing import Callable, Dict, TypeVar

from django.db.models import Model

from .exceptions import (
    CeleryNotEnabled,
    NotificationException,
    RelatedEventNotFound,
    RelatedSenderClassNotFound,
    RelatedUserNotFound,
    SenderSlugNotFoundException,
)
from .models import FollowUpEvent, Medium, NotificationEvent
from .utils import UserModel, is_installed

if sys.version_info >= (3, 3):
    from collections.abc import Iterable
else:
    from collections import Iterable


SenderType = TypeVar("SenderType", bound="NotificationSender")
CELERY_ENABLED = is_installed("celery")


if CELERY_ENABLED:
    from celery import group


class NotificationHandler:
    def __init__(self, ref_obj: Model, identifier: str) -> None:
        self.ref_obj = ref_obj
        self.identifier = identifier

    @cached_property
    def user(self) -> UserModel:
        if isinstance(self.ref_obj, UserModel):
            return self.ref_obj

        user = getattr(self.ref_obj, "user", None)

        if not user:
            raise RelatedUserNotFound("Reference object has not `user` attribute. ")

        return user

    @cached_property
    def event(self) -> NotificationEvent:
        notification = NotificationEvent.objects.filter(identifier=self.identifier).prefetch_related("mediums").first()

        if not notification:
            raise RelatedEventNotFound("No event found for identifier {}".format(self.identifier))

        return notification

    def replace_variables(self, text: str) -> str:
        replaced_text = text

        # Match `{{     ANY_TEXT }}`
        pattern = re.compile(r"({{\s*)(\w+)(\s*}})")
        matches = pattern.finditer(replaced_text)

        for match in matches:
            replaced_str = "".join(match.groups())
            field_name = match.group(2)

            replaced_text = replaced_text.replace(
                replaced_str,
                getattr(self.ref_obj, field_name, ""),
            )

        return replaced_text

    def generate_text_for_medium(self, medium: Medium):
        raw_text = self.event.get_text_for_medium(medium)
        return self.replace_variables(raw_text)

    @cached_property
    def all_senders(self) -> Dict[str, SenderType]:
        return {klass.SLUG: klass for klass in NotificationSender.__subclasses__()}

    def get_sender(self, medium: Medium) -> SenderType:
        klass = self.all_senders.get(medium.slug)

        if not klass:
            raise RelatedSenderClassNotFound(
                "Class for sending notification via {} not found. "
                "Class should have class attribute SLUG of {}, and it "
                "should be a subclass of NotificationSender class".format(
                    medium.label,
                    medium.slug,
                )
            )

        # return instance of sender class
        return klass()

    def get_sender_function(self, medium: Medium) -> Callable:
        klass = self.get_sender(medium)
        func = getattr(klass, "send", None)

        if not func:
            raise NotificationException("{} has no function `send`!".format(klass))

        if not callable(func):
            raise NotificationException("`send` attribute of {} class is not callable!".format(klass))

        return func

    def _send(self, medium: Medium, text: str):
        sender_function = self.get_sender_function(medium)

        if self.event.delay_seconds:
            if not CELERY_ENABLED:
                logging.warning("Celery is not enabled, will run tasks in foreground")
            else:
                pass

        sender_function(self.user, text)

    def handle_followup_events(self):
        if not CELERY_ENABLED:
            raise CeleryNotEnabled

        followup_events = FollowUpEvent.objects.filter(after_event=self.event, event__is_enabled=True)

        for f_event in followup_events:
            pass

    def send(self) -> None:
        for medium in self.event.mediums.all():
            text = self.generate_text_for_medium(medium)
            self._send(medium, text)
            self.handle_followup_events()


class NotificationSender:
    SLUG = None

    def __init__(self) -> None:
        if not self.SLUG:
            raise SenderSlugNotFoundException("Class did not define SLUG!")

    def send(self, user, text):
        raise NotImplementedError

    def bulk_send(self, users, texts):
        for user, text in zip(users, texts):
            self.send(user, text)
