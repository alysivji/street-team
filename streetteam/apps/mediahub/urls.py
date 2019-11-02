from django.urls import path
from apps.mediahub import views

urlpatterns = [
    path('', view=views.DebugView.as_view()),
]
