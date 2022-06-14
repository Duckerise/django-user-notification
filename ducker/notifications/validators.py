from django.apps import apps

from .exceptions import InvalidEventIdentifierFormat


def validate_event_identifier(value: str) -> None:
    if value:
        try:
            parts = value.split("__")
            app, model = parts[0], parts[1]
            apps.get_model(app, model)
        except IndexError:
            raise InvalidEventIdentifierFormat(
                "Invalid event identifier. Expected format %s__%s__%s"
            )
