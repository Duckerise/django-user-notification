import sys
from contextlib import nullcontext as does_not_raise

import pytest
from duckerise.notifications.exceptions import InvalidEventIdentifierFormat

from ..utils import uses_db
from ..validators import validate_event_identifier


@uses_db
@pytest.mark.parametrize(
    'exception,identifier', 
    [
        (does_not_raise(), 'auth__user'), 
        (pytest.raises(InvalidEventIdentifierFormat), 'auth_user'), 
        (pytest.raises(LookupError), 'auth__users')
    ]
)
def test_event_identifier_validator(exception, identifier):
    with exception:
        validate_event_identifier(identifier)
