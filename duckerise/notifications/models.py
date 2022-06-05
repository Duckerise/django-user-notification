from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .abc import AbstractNotifyEvent
from .utils import QuerySetType
from .validators import validate_event_identifier

UserModel: models.Model = get_user_model()


class Medium(models.Model):
    RAW_TEXT = 'raw_text'
    RICH_TEXT = 'rich_text'
    TEXT_FORMATS = ((RAW_TEXT, _('Raw text')), (RICH_TEXT, _('Rich text'))) 

    label: str =  models.CharField(max_length=63, blank=True, null=True)
    slug: str =  models.CharField(
        max_length=63, 
        unique=True, 
        help_text=_('The sender class name for this medium.')
    )
    text_format: str = models.CharField(
        max_length=15, 
        choices=TEXT_FORMATS, 
        help_text=_('Which type of text to send via this medium')
    )

    created_at: datetime = models.DateTimeField(auto_now_add=True)


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

    def get_text_for_medium(self, medium: Medium) -> str:
        # Will return either raw_text or rich_text
        return getattr(self, medium.text_format, '')

class OneTimeNotifyEvent(AbstractNotifyEvent):
    users: QuerySetType[UserModel] = models.ManyToManyField(UserModel)
    send_time: datetime = models.DateTimeField(_('Scheduled time'))


class FollowUpEvent(models.Model):
    event: NotificationEvent = models.ForeignKey(NotificationEvent, on_delete=models.CASCADE)
    after_event: NotificationEvent = models.ForeignKey(NotificationEvent, on_delete=models.CASCADE, related_name="followup_events")
    delay: int = models.PositiveIntegerField(help_text=_("The number of hours this event fire from related event"))
    frequency: int = models.PositiveIntegerField(help_text=_("This event will fire in every x hours"))
    count: int = models.PositiveIntegerField(help_text=_("The number of times this event will fire"))


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

