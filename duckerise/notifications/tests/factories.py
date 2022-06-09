import factory
from factory.django import DjangoModelFactory
from faker import Faker
from pytest_factoryboy import register

from ..models import Medium, NotificationEvent
from ..utils import UserModel

faker = Faker()


@register
class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel

    first_name = factory.LazyAttribute(lambda x: faker.name())
    username = factory.LazyAttribute(lambda x: faker.user_name())
    email = factory.LazyAttribute(lambda x: faker.email())


@register
class MediumFactory(DjangoModelFactory):
    class Meta:
        model = Medium

    label = factory.LazyAttribute(lambda x: faker.user_name())


@register
class NotificationEventFactory(DjangoModelFactory):
    class Meta:
        model = NotificationEvent

    label = factory.LazyAttribute(lambda x: faker.user_name())
