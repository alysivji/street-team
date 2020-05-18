from django.urls import path
from .views import TeamCreate, TeamDetailView

app_name = "teams"
urlpatterns = [
    path("teams/create/", view=TeamCreate.as_view(), name="create"),
    path("teams/<str:uuid>", view=TeamDetailView.as_view(), name="detail"),
]
