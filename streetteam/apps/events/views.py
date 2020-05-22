from django.views.generic.list import ListView

from .models import Event


class EventListView(ListView):
    model = Event
