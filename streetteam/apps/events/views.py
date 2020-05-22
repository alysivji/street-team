from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.views.generic.list import ListView

from .forms import EventDetailsForm
from .models import Event
from common.auth import AdminStaffRequiredMixin  # will need to clean this up


class EventListView(ListView):
    model = Event


class EventCreate(AdminStaffRequiredMixin, FormView):
    form_class = EventDetailsForm
    template_name = "events/event_form.html"

    def form_valid(self, form):
        # self.team_to_join = form.cleaned_data["join_code"]
        # user = self.request.user
        # add_user_to_team(user, self.team_to_join)
        return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self):
    #     return reverse("teams:detail", kwargs={"uuid": str(self.team_to_join.uuid)})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs.update({"user": self.request.user})
        return kwargs
