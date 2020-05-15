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

    @factory.post_generation
    def generate_upload_event(self, create, extracted, **kwargs):
        if not create:
            return
        UploadImageEventFactory(image=self, performed_by=self.uploaded_by)


class PostEventFactory(factory.DjangoModelFactory):
    class Meta:
        model = PostEvent

    name = "event"
    data = {}
    image = factory.SubFactory(UploadedImageFactory)
    performed_by = factory.SubFactory(UserFactory)


class UploadImageEventFactory(PostEventFactory):
    name = "upload_image"
    data = {}


class CropImageEventFactory(PostEventFactory):
    name = "crop_image"
    data = {"top": 0, "left": 0, "bottom": 50, "right": 50}


class AddCaptionEventFactory(PostEventFactory):
    name = "add_caption"
    data = {"caption": "Hanging out with the cr3w"}


class ModifyCaptionEventFactory(PostEventFactory):
    name = "modify_caption"
    data = {"caption": "Hanging out with the crew"}


class SubmitPostEventFactory(PostEventFactory):
    name = "submit_post"
    data = {}


class RejectPostEventFactory(PostEventFactory):
    name = "reject_post"
    data = {"reason": "None provided"}
