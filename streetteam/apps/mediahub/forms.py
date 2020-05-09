from django import forms


class UploadImagesForm(forms.Form):
    image = forms.FileField(
        label="Select pictures to upload", widget=forms.ClearableFileInput(attrs={"multiple": True})
    )
