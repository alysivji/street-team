import factory

from ..models import MediaResource, UploadedImage, PostEvent
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

    # https://factoryboy.readthedocs.io/en/latest/orms.html#factory.django.ImageField
    image = factory.django.ImageField(color="blue", width=100, height=100)
    uploaded_by = factory.SubFactory(UserFactory)


class PostEventFactory(factory.DjangoModelFactory):
    class Meta:
        model = PostEvent

    name = "event"
    data = {}
    image = factory.SubFactory(UploadedImageFactory)
    performed_by = factory.SubFactory(UserFactory)


class UploadImageEventFactory(PostEventFactory):
    name = "upload_image"
    data = {"width": 100, "height": 100}
    image = factory.SubFactory(UploadedImageFactory)
    performed_by = factory.SubFactory(UserFactory)
