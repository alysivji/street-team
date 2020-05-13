from typing import NamedTuple
from django import forms


class CropBox(NamedTuple):
    left: int
    top: int
    right: int
    bottom: int

    def to_dict(self):
        return {"left": self.left, "top": self.top, "right": self.right, "bottom": self.bottom}


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
