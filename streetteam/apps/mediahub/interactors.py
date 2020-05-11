from .models import UploadedImage


def handle_uploaded_file(user, info):
    uploaded_image = UploadedImage(user=user, **info)
    uploaded_image.save()
    print(2)


def go_crop_image(image, crop_box):
    image.crop(crop_box)
    # need to save
    # also need to link who did what
    # import pdb; pdb.set_trace()
    return True
