from faker_e164.providers import E164Provider
import factory

from ..models import PhoneNumber
from apps.users.tests.factories import UserFactory

faker = factory.Faker._get_faker()
faker.add_provider(E164Provider)


class PhoneNumberFactory(factory.DjangoModelFactory):
    class Meta:
        model = PhoneNumber

    number = factory.Faker("safe_e164", region_code="US")
    user = factory.SubFactory(UserFactory)
