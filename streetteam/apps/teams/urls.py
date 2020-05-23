from django.urls import path
from .views import TeamCreate, TeamDetailView, JoinTeamView, TeamListView, new_join_code_view
from apps.events.views import TeamEventListView, EventCreate

app_name = "teams"
urlpatterns = [
    path("teams/<str:uuid>/events/", view=TeamEventListView.as_view(), name="events"),
    path("teams/<str:uuid>/events/new", view=EventCreate.as_view(), name="create-event"),
    path("teams/create/", view=TeamCreate.as_view(), name="create"),
    path("teams/join/", view=JoinTeamView.as_view(), name="join"),
    path("teams/<str:uuid>/modify-joincode", view=new_join_code_view, name="modify-joincode"),
    path("teams/<str:uuid>", view=TeamDetailView.as_view(), name="detail"),
    path("teams", view=TeamListView.as_view(), name="list"),
]
