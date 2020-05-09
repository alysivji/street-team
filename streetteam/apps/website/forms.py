from django import forms


class UploadFileForm(forms.Form):
    file_field = forms.FileField(
        label="Select pictures to upload", widget=forms.ClearableFileInput(attrs={"multiple": True})
    )
