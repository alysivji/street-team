from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
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


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect("/success/url/")
    else:
        form = UploadFileForm()
    return render(request, "load_images.html", {"form": form})
