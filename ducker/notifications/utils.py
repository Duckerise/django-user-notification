from typing import Generic, Iterable, Optional, TypeVar

import pytest
from django.contrib.auth import get_user_model
from django.db.models import Model, QuerySet

##### QuerySet as type for type hinting #####
_T = TypeVar("_T", bound=Model)


class QuerySetType(Generic[_T], QuerySet):
    def __iter__(self) -> Iterable[_T]:
        pass

    def first(self) -> Optional[_T]:
        pass


##### User Model #####
UserModel: Model = get_user_model()

##### Pytest #####
uses_db = pytest.mark.django_db

##### Other utilities #####
def is_installed(package):
    try:
        __import__(package)
        return True
    except ImportError:
        return False
