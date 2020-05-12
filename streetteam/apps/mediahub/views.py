from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .forms import UploadImagesForm, CropImageParametersForm
from .interactors import crop_image, handle_uploaded_file
from .models import UploadedImage


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
def crop_image_view(request, pk):
    form = CropImageParametersForm(request.POST)
    if form.is_valid():
        crop_image(user=request.user, image_id=pk, crop_box=form.cleaned_data)
        # get the uuid and go to the next page
        return JsonResponse({"success": True})
    else:
        # go back to detail view
        return JsonResponse({"success": False})
