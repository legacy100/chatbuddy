from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# the message import is used to output error messages and warning messages 
from django.contrib import messages
# the login_required decorator is used to make sure that the user is logged in before they can access the page
from django.contrib.auth.decorators import login_required
# The Q import is used to output the filtered results to the console
from django.db.models import Q
# import user is used to retrieve the user from the database
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, MessageForm

# Create your views here.
# rooms = [
#     {'id': 1, 'name': 'This is Room 1'},
#     {'id': 2, 'name': 'This is Room 2'},
#     {'id': 3, 'name': 'This is Room 3'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
        

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
# check if the user exists from the imported User Model, if not just throw up an error
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
# if a user exists go ahead and authenticate/check if the login details are correct
        user = authenticate(request, username=username, password=password)
# if the details are correct, go ahead and log the user in and create a session
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password does not exist')


    content={'page':page}
    return render(request, 'chatbase/login_register.html', content)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
# The UserCreationForm will Auto create the user register form
    form = UserCreationForm()
# Pass in the user data
    if request.method == 'POST':
# Pass the Data into the user creation form
        form = UserCreationForm(request.POST)
# Check if the form is valid
        if form.is_valid():
# if a form is created is valid, Commit is set to false to access the register input immediately 
            user = form.save(commit=False)
# Access the user immediately and convert it to lower case
            user.username = user.username.lower()
#  Get the user and save the user data
            user.save()
# login the user
            login(request, user)
# redirect the user to the home page
            return redirect('home')
        
        else:
            messages.error(request, 'An Error Occured during registration')

    return render(request, 'chatbase/login_register.html', {'form':form})

def home(request):
# This function is going to filter the data output so that when you click on a particular topic only the item under the topic tag will be displayed, and run the inline if statement.
    q = request.GET.get('q') if request.GET.get('q') != None else ''
# The value "__icontains" will filter the value typed in the search space or url will find a match in the topic then display the related topic tag.
    rooms = Room.objects.filter(
# here we add all the search field to filter through topic, name and description
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    
    topics = Topic.objects.all()
# rooms.count is to get the number of rooms filtered from the searche engine
    room_count = rooms.count()
# .order_by is to get the order of the message comments and limit the output to 5
    room_messages = Message.objects.all().order_by('-created')[:4]
    
    content = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'room_messages': room_messages}
    return render(request, 'chatbase/home.html', content)

# refer/call the dynamic url from the url file by using the pk
def room(request, pk):
    room = Room.objects.get(id=pk)
# message_set.all() is used to get all the attributes of the Message model which is the child to a Parent Room Model and itcan be accessed in a lower case --> that is to say "import all the messages attributed to this room".
    chat_messages = room.message_set.all().order_by('-created') 
    participants = room.participants.all()
# when a user comments in a group, this if statement will send the message to the same group as a chat
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
# the participants.add method adds a user to the participant list when a user comments or sends a message
        room.participants.add(request.user)
# the dynameic value pk=room.id is going to get the input message and output the message in the chat room and refresh the page
        return redirect('room', pk=room.id)

    content = {'room': room, 'chat_messages': chat_messages, 'participants': participants}
    return render(request, 'chatbase/room.html', content)


# if user is authenticated then he can create a room else restrict and redirect to login page
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        # print(request.POST) for debugging reference
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    content = {'form': form}
    return render(request, 'chatbase/chat_form.html', content)


# if user is authenticated then he can update a room else restrict and redirect to login page
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
# the 'instance' key will bring the data when the edit button is clicked 
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You do not have permission to edit this room, make sure you are the host')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    content = {'form':form}
    return render(request, 'chatbase/chat_form.html', content)


# if user is authenticated then he can delete a room else restrict and redirect to login page
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You do not have permission to delete this room, make sure you are the host')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'chatbase/delete.html', {'obj':room})


@login_required(login_url='login')
def editMessage(request, pk):
    chat = Message.objects.get(id=pk)
    chatedit = MessageForm(instance=chat)


    if request.method == 'POST':
        chatedit = MessageForm(request.POST, instance=chat)
        if chatedit.is_valid():
            chatedit.save()
            return redirect('home')

    content = {'chatedit':chatedit}
    return render(request, 'chatbase/edit_chat.html', content)



@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You do not have permission to delete this room, make sure you are the host')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'chatbase/delete.html', {'obj':message})


