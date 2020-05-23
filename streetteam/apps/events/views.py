from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.views.generic.list import ListView

from .forms import EventInformationForm
from .interactors import create_event
from .models import Event
from common.auth import TeamAdminRoleRequiredMixin


class EventListView(ListView):
    model = Event


class TeamEventListView(ListView):
    # TODO this is just like events by for a single team
    # TODO return a team only queryset
    model = Event


class EventCreate(TeamAdminRoleRequiredMixin, FormView):
    form_class = EventInformationForm
    template_name = "events/event_form.html"

    def form_valid(self, form):
        self.team = form.cleaned_data.pop("team")
        user = self.request.user
        create_event(user, self.team, form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        # TODO take to a save as drafts / publish page
        return reverse("teams:events", kwargs={"uuid": str(self.team.uuid)})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user, "team_uuid": self.kwargs["uuid"]})
        return kwargs


class EventDetailView(DetailView):
    model = Event

    def get_object(self):
        return self.model.objects.get(uuid=self.kwargs["uuid"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {"event_uuid": self.kwargs["uuid"]}
        return context
