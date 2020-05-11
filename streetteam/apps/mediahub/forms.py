from django import forms


class UploadImagesForm(forms.Form):
    image = forms.FileField(
        label="Select pictures to upload", widget=forms.ClearableFileInput(attrs={"multiple": True})
    )


class CropImageParametersForm(forms.Form):
    cropLeft = forms.FloatField()
    cropTop = forms.FloatField()
    cropWidth = forms.FloatField()
    cropHeight = forms.FloatField()
