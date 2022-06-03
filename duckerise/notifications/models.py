from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from duckerise.notifications.abc import AbstractNotifyEvent
from duckerise.notifications.validators import validate_event_identifier

# Create your models here.

class NotificationEventTemplate(AbstractNotifyEvent):

    identifier: str = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        unique=True,
        validators=[validate_event_identifier],
    )
    delay_seconds: int = models.PositiveIntegerField(
        default=0,
        help_text=_("Number of seconds to postpone the notifications send"),
    )

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label

class FollowUpEvent(models.Model):
    pass


class Medium(models.Model):
    pass

class NotificationHistory(models.Model):
    pass

