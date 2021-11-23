from django.shortcuts import render, redirect
from django.http import HttpResponse
# render model Room in
from .models import Room
from .forms import RoomForm

# Create your views here.
# multi-line command = ctrl + k + ctrl + c
# rooms = [
#     {'id': 1, 'name': 'Lets learn python'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]

def home(request):
    # add Room objects in home page
    # it can let us make query to database
    # queryset = ModelName.objects.all()
    # variable = name.objectsattribute.method(.get/.filter/.exclude)
    # models auto generate id for them
    # this will replace the original rooms list to our Room model database
    rooms = Room.objects.all() # all give us all Rooms in database
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    # get Room unique single value
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

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
def updateRoom(request, pk):
    # query
    room = Room.objects.get(id=pk)
    # know which room to update
    form = RoomForm(instance=room)

    if request.method == 'POST':
        # need to tell which room to update
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)