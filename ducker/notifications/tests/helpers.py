from dataclasses import dataclass

from ..utils import UserModel


@dataclass
class RefObjClass:
    user: UserModel


@dataclass
class NonRefObjClass:
    pass
