from django.urls import path
from .views import TeamCreate, TeamDetailView, JoinTeamView, TeamListView

app_name = "teams"
urlpatterns = [
    path("teams/create/", view=TeamCreate.as_view(), name="create"),
    path("teams/join/", view=JoinTeamView.as_view(), name="join"),
    path("teams/<str:uuid>", view=TeamDetailView.as_view(), name="detail"),
    path("teams", view=TeamListView.as_view(), name="list"),
]
