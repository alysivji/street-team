from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View


class IndexView(TemplateView):

    template_name = "index.html"


class AccountView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = request.user
        context = {"user": user}
        return render(request, "user_details.html", context)
