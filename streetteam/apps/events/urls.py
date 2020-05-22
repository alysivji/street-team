from django.urls import path
from .views import EventListView, EventCreate

app_name = "events"
urlpatterns = [
    path("events", view=EventListView.as_view(), name="list"),
    path("events/new", view=EventCreate.as_view(), name="create"),
]
