from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "duckerise.notifications"
    label = "duckerise_notifications"
    verbose_name = _("Duckerise Notifications")
