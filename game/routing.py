# game/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/reversi/<str:room_name>/', consumers.ReversiConsumer.as_asgi()),
]
