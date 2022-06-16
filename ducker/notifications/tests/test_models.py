import pytest

from ..utils import uses_db
from .factories import MediumFactory, NotificationEventFactory


@uses_db
@pytest.mark.parametrize(
    "text_format",
    [
        "raw_text",
        "rich_text",
    ],
)
def test_get_text_for_medium(text_format):
    event = NotificationEventFactory(raw_text="raw_text", rich_text="rich_text")
    medium = MediumFactory(text_format=text_format)

    assert event.get_text_for_medium(medium) == text_format
