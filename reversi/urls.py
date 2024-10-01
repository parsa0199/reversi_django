# reversi/urls.py

from django.urls import path
from .views import reversi_view

urlpatterns = [
    path('', reversi_view, name='game'),
]
