from typing import NamedTuple
from django import forms


class CropBox(NamedTuple):
    left: int
    top: int
    right: int
    bottom: int


class UploadImagesForm(forms.Form):
    image = forms.FileField(
        label="Select pictures to upload", widget=forms.ClearableFileInput(attrs={"multiple": True})
    )


class CropImageParametersForm(forms.Form):
    cropLeft = forms.FloatField()
    cropTop = forms.FloatField()
    cropWidth = forms.FloatField()
    cropHeight = forms.FloatField()

    def clean(self):
        cleaned_data = super().clean()
        top = cleaned_data["cropTop"]
        left = cleaned_data["cropLeft"]
        bottom = top + cleaned_data["cropHeight"]
        right = left + cleaned_data["cropWidth"]
        return CropBox(left=left, top=top, right=right, bottom=bottom)


class CaptionImageForm(forms.Form):
    caption = forms.CharField(
        label="Caption image", widget=forms.Textarea(attrs={"id": "imageCaption", "placeholder": "", "rows": 5})
    )
    uuid = forms.CharField(widget=forms.TextInput(attrs={"id": "modalUuid", "hidden": True}))

    def clean_caption(self):
        # check to make sure tweet is less than 280 characters
        pass

    # def clean(self):
    #     from .models import UploadedImage

    #     cleaned_data = super().clean()
    #     uuid = cleaned_data["uuid"]
    #     image = UploadedImage.objects.filter(uuid=uuid)
    #     if not image:
    #         raise forms.ValidationError("Not a valid image")
    #     return image
