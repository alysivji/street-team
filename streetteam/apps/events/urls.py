from django.urls import path
from .views import EventListView

app_name = "events"
urlpatterns = [path("events", view=EventListView.as_view(), name="list")]
