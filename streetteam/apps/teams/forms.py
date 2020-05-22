from django import forms

from .models import Team


class EnterJoinCodeForm(forms.Form):
    join_code = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_join_code(self):
        join_code = self.cleaned_data.get("join_code")
        try:
            team_to_join = Team.objects.get(join_code=join_code)
        except Team.DoesNotExist:
            raise forms.ValidationError("Invalid join code. Please talk to team owner")

        if self.user in team_to_join.memberships.get_members():
            raise forms.ValidationError("You are already part of the team!")

        return team_to_join
