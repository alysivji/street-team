from django import forms
from multiupload.fields import MultiImageField


class UploadFileForm(forms.Form):
    images = MultiImageField(min_num=1)
