from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View

from .forms import UploadFileForm


class IndexView(TemplateView):

    template_name = "index.html"


class AccountView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = request.user
        context = {"user": user}
        return render(request, "user_details.html", context)


@login_required
def upload_file(request):
    request.FILES.getlist("file_field")
    num_processed = num_not_valid = 0
    if request.method == "POST":
        for image in request.FILES.getlist("file_field"):
            file_data = {"file_field": image}
            form = UploadFileForm(request.POST, file_data)
            if form.is_valid():
                # handle_uploaded_file(request.FILES['file'])
                num_processed += 1
            else:
                print("did not process")
                num_not_valid += 1
        return JsonResponse({"num_processed": num_processed, "num_not_valid": num_not_valid})
    else:
        form = UploadFileForm()
    return render(request, "form.html", {"form": form})
