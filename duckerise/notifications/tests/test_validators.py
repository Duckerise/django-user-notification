import sys
from contextlib import nullcontext as does_not_raise

import pytest
from duckerise.notifications.exceptions import InvalidEventIdentifierFormat

from ..utils import uses_db
from ..validators import validate_event_identifier


@uses_db
def test_event_identifier_validator():
    with does_not_raise():
        validate_event_identifier("auth__user")

@uses_db
def test_event_identifier_validator2():
    with pytest.raises(InvalidEventIdentifierFormat):
        validate_event_identifier("auth_user")

@uses_db
def test_event_identifier_validator3():
    with pytest.raises(LookupError):
        validate_event_identifier("auth__users")
