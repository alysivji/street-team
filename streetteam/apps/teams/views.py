from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import EnterJoinCodeForm
from .interactors import add_user_to_team, make_user_admin_of_team
from .models import Team
from common.auth import AdminStaffRequiredMixin


class TeamCreate(AdminStaffRequiredMixin, CreateView):
    model = Team
    fields = ["name"]

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        make_user_admin_of_team(self.request.user, team=self.object)
        return HttpResponseRedirect(self.get_success_url())


class JoinTeamView(FormView):
    form_class = EnterJoinCodeForm
    template_name = "teams/team_enter_join_code.html"

    def form_valid(self, form):
        self.team_to_join = form.cleaned_data["join_code"]
        user = self.request.user
        add_user_to_team(user, self.team_to_join)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("teams:detail", kwargs={"uuid": str(self.team_to_join.uuid)})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class TeamDetailView(DetailView):
    model = Team

    def get_object(self):
        return self.model.objects.get(uuid=self.kwargs["uuid"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            "name": self.object.name,
            "join_code": self.object.join_code,
            "users": self.object.memberships.get_members(),
            "now": timezone.now(),
        }
        return context


class TeamListView(ListView):
    model = Team
