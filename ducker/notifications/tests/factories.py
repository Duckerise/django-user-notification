from typing import Generic, TypeVar

import factory
from factory import Factory
from factory.django import DjangoModelFactory
from faker import Faker
from pytest_factoryboy import register

from ..handler import NotificationHandler
from ..models import (
    FollowUpEvent,
    Medium,
    NotificationEvent,
    NotificationHistory,
    OneTimeNotifyEvent,
)
from ..utils import UserModel

faker = Faker()

##### Base Meta Factory for Type Hinting #####

# Taken from
# https://github.com/FactoryBoy/factory_boy/issues/468#issuecomment-1151633557
T = TypeVar("T")


class BaseMetaFactory(Generic[T], factory.base.FactoryMetaClass):
    def __call__(cls, *args, **kwargs) -> T:
        return super().__call__(*args, **kwargs)


##### Django Model Factories #####
@register
class UserFactory(DjangoModelFactory, metaclass=BaseMetaFactory[UserModel]):
    class Meta:
        model = UserModel

    first_name = factory.LazyAttribute(lambda x: faker.name())
    username = factory.LazyAttribute(lambda x: faker.user_name())
    email = factory.LazyAttribute(lambda x: faker.email())


@register
class MediumFactory(DjangoModelFactory, metaclass=BaseMetaFactory[Medium]):
    class Meta:
        model = Medium

    label = faker.user_name()
    slug = label.lower()
    text_format = Medium.RAW_TEXT


class AbstractNotificationEventFactory(DjangoModelFactory):
    class Meta:
        abstract = True

    label: str = factory.LazyAttribute(lambda x: faker.user_name())
    raw_text = faker.text()
    rich_text = raw_text
    is_active = True

    @factory.post_generation
    def mediums(self, create, extracted, **kwargs):
        if extracted:
            for medium in extracted:
                self.mediums.add(medium)


@register
class NotificationEventFactory(
    AbstractNotificationEventFactory,
    metaclass=BaseMetaFactory[NotificationEvent],
):
    class Meta:
        model = NotificationEvent

    delay_seconds = 0


@register
class OneTimeNotifyEventFactory(
    AbstractNotificationEventFactory,
    metaclass=BaseMetaFactory[OneTimeNotifyEvent],
):
    class Meta:
        model = OneTimeNotifyEvent

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if extracted:
            for user in extracted:
                self.users.add(user)


@register
class FollowUpEventFactory(
    AbstractNotificationEventFactory,
    metaclass=BaseMetaFactory[FollowUpEvent],
):
    class Meta:
        model = FollowUpEvent

    event = factory.SubFactory(NotificationEventFactory)
    after_event = factory.SubFactory(NotificationEventFactory)

    delay = 0
    frequency = 1
    count = 1


@register
class NotificationHistoryFactory(
    DjangoModelFactory,
    metaclass=BaseMetaFactory[NotificationHistory],
):
    event = factory.SubFactory(NotificationEventFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = NotificationHistory


##### Other Factories #####
class NotificationHandlerFactory(
    Factory,
    metaclass=BaseMetaFactory[NotificationHandler],
):
    class Meta:
        model = NotificationHandler

    ref_obj = None
    identifier = None
