from django.urls import path
from .views import EventDetailView, EventListView

app_name = "events"
urlpatterns = [
    path("events", view=EventListView.as_view(), name="list"),
    path("events/<str:uuid>", view=EventDetailView.as_view(), name="detail"),
]
