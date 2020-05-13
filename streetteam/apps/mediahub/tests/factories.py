import factory

from ..models import MediaResource, UploadedImage, UploadedImageEvent
from apps.twilio_integration.tests.factories import PhoneNumberFactory
from apps.users.tests.factories import UserFactory


class MediaResourceFactory(factory.DjangoModelFactory):
    class Meta:
        model = MediaResource

    resource_url = factory.Faker("url")
    phone_number = factory.SubFactory(PhoneNumberFactory)


class UploadedImageFactory(factory.DjangoModelFactory):
    class Meta:
        model = UploadedImage

    image = factory.django.ImageField(color="blue", width=100, height=100)
    uploaded_by = factory.SubFactory(UserFactory)


class UploadedImageEventFactory(factory.DjangoModelFactory):
    class Meta:
        model = UploadedImageEvent
