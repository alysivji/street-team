from django import forms

from .models import Team


class EnterJoinCodeForm(forms.Form):
    uuid = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_uuid(self):
        joined_code = self.cleaned_data.get("uuid")
        try:
            team_to_join = Team.objects.get(join_code=joined_code)
        except Team.DoesNotExist:
            raise forms.ValidationError("Invalid join code. Please talk to team owner")

        if self.user in team_to_join.memberships.get_members():
            raise forms.ValidationError("You are already part of the team!")

        return team_to_join
