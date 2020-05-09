from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .forms import UploadImagesForm
from .interactors import handle_uploaded_file


@login_required
def upload_file(request):
    request.FILES.getlist("image")
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
