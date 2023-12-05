from django.urls import path

from tickets.views import TicketAPIView

urlpatterns = [
    path('', TicketAPIView.as_view(), name='ticket-create'),
]