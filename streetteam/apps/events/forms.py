from datetime import datetime, timezone

from django import forms

from .models import Event
from apps.teams.models import Team


class EventInformationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "happens_on"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.team_uuid = kwargs.pop("team_uuid", None)
        super().__init__(*args, **kwargs)

    def clean_happens_on(self):
        # TODO think thru timezones
        # user always sees information in their timezone
        # we always compare against UTC
        # how do comparisons work?
        event_date = self.cleaned_data["happens_on"]
        # TODO can only create events x amount of time in the future
        if event_date <= datetime.now(timezone.utc):
            raise forms.ValidationError("Event needs to be in the future")
        return event_date

    def clean(self):
        try:
            team = Team.objects.get(uuid=self.team_uuid)
        except Team.DoesNotExist:
            raise forms.ValidationError("Invalid entry. Please talk to site administrator")

        if self.user not in team.memberships.get_leadership():
            raise forms.ValidationError("You are not authorized to make this change. Please talk to Team Leader.")

        self.cleaned_data["team"] = team
        return self.cleaned_data
