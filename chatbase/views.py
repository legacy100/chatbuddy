from django.shortcuts import render
# from sympy import content
from .models import Room

# Create your views here.
# rooms = [
#     {'id': 1, 'name': 'This is Room 1'},
#     {'id': 2, 'name': 'This is Room 2'},
#     {'id': 3, 'name': 'This is Room 3'},
# ]

def home(request):
    rooms = Room.objects.all()
    content = {'rooms': rooms}
    return render(request, 'chatbase/home.html', content)

# refer/call the dynamic url from the url file by using the pk
def room(request, pk):
    room = Room.objects.get(id=pk)
    content = {'room': room}
    return render(request, 'chatbase/room.html', content)

def createChat(request):
    content = {} 
    return render(request, 'chatbase/chat_form.html', content)