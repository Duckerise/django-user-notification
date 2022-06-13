from typing import TYPE_CHECKING

from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import QuerySetType

if TYPE_CHECKING:
    from .models import Medium


class AbstractNotifyEvent(models.Model):
    label: str = models.CharField(max_length=100, unique=True)
    mediums: QuerySetType["Medium"] = models.ManyToManyField(
        "duckerise_notifications.Medium"
    )
    raw_text: str = models.TextField(
        help_text=_(
            "Raw text, which can be used for sending SMS or similar mediums. Empty text won't be sent."
        ),
        blank=True,
        null=True,
    )
    rich_text: str = RichTextField(
        help_text=_(
            "Formatted text, which can be used for sending email or similar mediums. Empty text won't be sent."
        ),
        blank=True,
        null=True,
    )
    is_active: bool = models.BooleanField(
        default=True,
        verbose_name=_("Notification is active"),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.label
