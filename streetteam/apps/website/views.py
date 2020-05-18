from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View


class IndexView(TemplateView):

    template_name = "index.html"


class AccountView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = request.user
        context = {
            "user": user,
            "teams": user.memberships.get_teams(),
            "events": user.events.all(),
            "submissions": user.uploaded_images.all(),
        }
        # TODO use a manager to get teams
        return render(request, "user_details.html", context)


def logout_view(request):
    logout(request)
    return redirect("index")
