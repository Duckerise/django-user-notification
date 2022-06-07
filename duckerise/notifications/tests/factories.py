import factory
import faker
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

UserModel = get_user_model()
fake = faker.Factory.create()


@register
class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel

    first_name = factory.LazyAttribute(lambda x: fake.name())
    username = factory.LazyAttribute(lambda x: fake.name())
    email = factory.LazyAttribute(lambda x: fake.email())
