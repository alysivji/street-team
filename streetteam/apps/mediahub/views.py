from typing import NamedTuple

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from PIL import Image

from .forms import UploadImagesForm, CropImageParametersForm
from .interactors import handle_uploaded_file, go_crop_image
from .models import UploadedImage


class CropBox(NamedTuple):
    left: int
    top: int
    right: int
    bottom: int

    @classmethod
    def from_cleaned_form_data(cls, data):
        top = data["cropTop"]
        left = data["cropLeft"]
        bottom = top + data["cropHeight"]
        right = left + data["cropWidth"]
        return cls(left=left, top=top, right=right, bottom=bottom)


@login_required
def upload_file(request):
    num_processed = num_not_valid = 0
    if request.method == "POST":
        for image in request.FILES.getlist("image"):
            file_data = {"image": image}
            form = UploadImagesForm(request.POST, file_data)
            if form.is_valid():
                handle_uploaded_file(request.user, form.files)
                num_processed += 1
            else:
                print("did not process")
                num_not_valid += 1
        return JsonResponse({"num_processed": num_processed, "num_not_valid": num_not_valid})
    else:
        form = UploadImagesForm()
    return render(request, "form.html", {"form": form})


class UploadedImagesListView(ListView):

    model = UploadedImage
    paginate_by = 10  # if pagination is desired
    template_name = "list.html"


class UploadedImagesDetailView(DetailView):

    model = UploadedImage
    template_name = "crop.html"


@login_required
def crop_image(request, pk):
    form = CropImageParametersForm(request.POST)
    if form.is_valid():
        # pass the image id
        # pass the dropbox
        image = Image.open(UploadedImage.objects.get(pk=pk).image)
        box = CropBox.from_cleaned_form_data(form.cleaned_data)
        go_crop_image(image, box)

        return JsonResponse({"success": True})
    else:
        # go back to detail view
        return JsonResponse({"success": False})
