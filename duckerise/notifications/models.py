from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from duckerise.notifications.abc import AbstractNotifyEvent
from duckerise.notifications.validators import validate_event_identifier

from .utils import QuerySetType

# Create your models here.
UserModel = get_user_model()

class NotificationEvent(AbstractNotifyEvent):
    identifier: str = models.CharField(
        max_length=64,
        unique=True,
        validators=[validate_event_identifier],
    )
    delay_seconds: int = models.PositiveIntegerField(
        default=0,
        help_text=_('Number of seconds to postpone the notifications send'),
    )

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

class OneTimeNotifyEvent(AbstractNotifyEvent):
    users: QuerySetType[UserModel] = models.ManyToManyField(UserModel)
    send_time: datetime = models.DateTimeField(_('Scheduled time'))


class FollowUpEvent(models.Model):
    event: NotificationEvent = models.ForeignKey(NotificationEvent, on_delete=models.CASCADE)
    after_event: NotificationEvent = models.ForeignKey(NotificationEvent, on_delete=models.CASCADE, related_name="followup_events")
    delay: int = models.PositiveIntegerField(help_text=_("The number of hours this event fire from related event"))
    frequency: int = models.PositiveIntegerField(help_text=_("This event will fire in every x hours"))
    count: int = models.PositiveIntegerField(help_text=_("The number of times this event will fire"))


class Medium(models.Model):
    label: str =  models.CharField(max_length=63, blank=True, null=True)
    slug: str =  models.CharField(max_length=63, unique=True)

    created_at: datetime = models.DateTimeField(auto_now_add=True)

class NotificationHistory(models.Model):
    event: NotificationEvent = models.ForeignKey(
        NotificationEvent,
        on_delete=models.PROTECT,
        related_name='notifications',
    )
    user: UserModel = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='notifications')
    ref_id: str = models.CharField(max_length=150, blank=True, null=True)
    
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

