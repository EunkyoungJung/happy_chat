# chat/views.py
from django.shortcuts import render

from .auth import generate_username

def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    username_candidate = generate_username()

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username_candidate': generate_username(),
    })
