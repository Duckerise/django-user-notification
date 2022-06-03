from typing import TYPE_CHECKING

from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from notifications.models import Medium


class AbstractNotifyEvent(models.Model):
    label: str = models.CharField(max_length=100, unique=True)
    medium: "Medium" = models.ForeignKey("notifications.Medium", blank=True, null=True, on_delete=models.SET_NULL)
    raw_text: str = models.TextField(help_text=_("Raw text, which can be used for sending SMS or similar mediums. Empty text won't be sent.", blank=True, null=True))
    formatted_text: str = RichTextField(help_text=_("Formatted text, which can be used for sending email or similar mediums. Empty text won't be sent.", blank=True, null=True))
    is_enabled: bool = models.BooleanField(
        default=True, verbose_name=_("Notifications enabled")
    )

    class Meta:
        abstract = True
