from django.urls import path

from teams.views import TeamCreateAPIView

urlpatterns = [
    path('', TeamCreateAPIView.as_view(), name='team-create'),
]
