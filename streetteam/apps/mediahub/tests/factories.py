import factory

from ..models import MediaResource
from apps.twilio_integration.tests.factories import PhoneNumberFactory


class MediaResourceFactory(factory.DjangoModelFactory):
    class Meta:
        model = MediaResource

    resource_url = factory.Faker("url")
    phone_number = factory.SubFactory(PhoneNumberFactory)
