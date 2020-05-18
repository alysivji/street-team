from django.urls import path
from .views import TeamCreate, TeamDetailView

urlpatterns = [
    path("teams/create/", view=TeamCreate.as_view(), name="team-create"),
    path("teams/<str:uuid>", view=TeamDetailView.as_view(), name="team-detail"),
]
