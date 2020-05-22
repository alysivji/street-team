from django.forms import ModelForm

from .models import Event


class EventDetailsForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "happens_on"]
