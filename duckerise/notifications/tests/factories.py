import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from faker import Faker
from pytest_factoryboy import register

UserModel = get_user_model()
faker = Faker()


@register
class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel

    first_name = factory.LazyAttribute(lambda x: faker.name())
    username = factory.LazyAttribute(lambda x: faker.user_name())
    email = factory.LazyAttribute(lambda x: faker.email())
