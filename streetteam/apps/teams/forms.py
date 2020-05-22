from django import forms

from .models import Team


class EnterJoinCodeForm(forms.Form):
    uuid = forms.CharField()

    def clean_uuid(self):
        joined_code = self.cleaned_data.get("uuid")
        try:
            team_to_join = Team.objects.get(join_code=joined_code)
        except Team.DoesNotExist:
            raise forms.ValidationError("Invalid join code. Please talk to team owner")
        return team_to_join
