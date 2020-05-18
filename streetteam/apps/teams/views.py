from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .interactors import add_user_team_relationship
from .models import Team
from common.auth import AdminStaffRequiredMixin


class TeamCreate(AdminStaffRequiredMixin, CreateView):
    model = Team
    fields = ["name"]

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        add_user_team_relationship(self.request.user, team=self.object)
        return HttpResponseRedirect(self.get_success_url())


class TeamDetailView(DetailView):
    model = Team

    def get_object(self):
        return self.model.objects.get(uuid=self.kwargs["uuid"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {"users": self.object.memberships.get_users(), "now": timezone.now()}
        return context
