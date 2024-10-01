# game/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'game/index.html')

def game_room(request, room_name):
    return render(request, 'game/game_room.html', {
        'room_name': room_name
    })
