from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "duckerise.notifications"
    label = "duckerise_notifications"
    verbose_name = _("Duckerise Notifications")
