from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# render model Room in
from .models import Room, Topic, Message
from .forms import RoomForm


# Create your views here.
# multi-line command = ctrl + k + ctrl + c
# rooms = [
#     {'id': 1, 'name': 'Lets learn python'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]

# dont use def login(), cause it already exists
def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # only user lowercase
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exitst')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    # we have UserCreationForm -> dont need register page
    # page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        # pass our username, password etc information to server
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # we need to deal the data first, so we just save it first
            # but not commit
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    # add Room objects in home page
    # it can let us make query to database
    # queryset = ModelName.objects.all()
    # variable = name.objectsattribute.method(.get/.filter/.exclude)
    # models will auto generate id for them
    # this will replace the original rooms list to our Room model database
    # rooms = Room.objects.all() # all give us all Rooms in database
    # we don't want all, we only want to show the chosen one
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # query nothing -> query everything -> output everything with __name_contains
    # "i" means insensitive -> value can be lower or uppercase 
    rooms = Room.objects.filter(
        # with Q, we can add logic
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    # Topic side bar
    topics = Topic.objects.all()

    # this is faster than len(rooms)
    room_count = rooms.count()

    # shows with specific urls
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,
               'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    # get Room unique single value
    room = Room.objects.get(id=pk)
    # query .model.message -> get all messages that related to this room
    room_messages = room.message_set.all() # .order_by('-create') because we did this in class Message
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        # add commentor in participants(many to many field)
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

# if not login -> redirect user to login page
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        # this print all the data
        # print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

# pk=primary key
# know what item is updating
@login_required(login_url='login')
def updateRoom(request, pk):
    # query
    room = Room.objects.get(id=pk)
    # know which room to update
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')

    if request.method == 'POST':
        # need to tell which room to update
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

# add primary key -> which room are we deleting
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})