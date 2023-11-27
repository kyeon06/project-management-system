from django.urls import path

from teams.views import TeamCreateAPIView, TeamInviteAPIView

urlpatterns = [
    path('', TeamCreateAPIView.as_view(), name='team-create'),
    path('<int:team_id>/invite/', TeamInviteAPIView.as_view(), name='team-invite'),
]
