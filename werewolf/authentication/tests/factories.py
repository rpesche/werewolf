import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):

    username = factory.Faker('name')
    email = factory.LazyAttribute(lambda user: f'{user.username}@test.com')

    class Meta:
        model = get_user_model()
