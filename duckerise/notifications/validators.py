from django.apps import apps
from django.forms import ValidationError


def validate_event_identifier(value: str):
    if value:
        try:
            parts = value.split("__")
            app, model = parts[0], parts[1]
            apps.get_model(app, model)
        except (IndexError, LookupError):
            raise ValidationError("Invalid event identifier")
