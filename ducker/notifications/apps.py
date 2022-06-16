from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ducker.notifications"
    label = "ducker_notifications"
    verbose_name = _("Ducker Notifications")
