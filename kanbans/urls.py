from django.urls import path

from kanbans.views import ColumnAPIView


urlpatterns = [
    path('columns/', ColumnAPIView.as_view()),
    
]
