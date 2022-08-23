from itertools import count
from django.shortcuts import render,redirect
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q

# Create your views here.



# rooms=[
#     {'id':1,'name':'Purnima'},
#     {'id':2,'name':'Yatin'},
#     {'id':3,'name':'Irfan'},

# ]
def home(request):
    topics=Topic.objects.all()
    rom=Room.objects.all()
    count_list={}
    for i in topics:
        counter=0
        for j in rom:
            if j.topic==i:
                counter=counter+1
        count_list[i.name]=counter

    if request.GET.get('q') != None:
        q=request.GET.get('q')
    else:
        q=''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(name__icontains=q)
    )



    rooms_c=Room.objects.all().count()


    context={'room':rooms,'topic':topics,'count':rooms_c,'count_list':count_list}
    return render(request,'home/home.html',context)


def room(request,pk):
    room=Room.objects.get(id=pk)

    context={'room':room}
    return render(request,'home/room.html',context)



def createRoom(request):
    form=RoomForm()
    if request.method=="POST":
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'home/room_form.html',context)



def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.method=="POST":
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'home/room_form.html',context)
 

# def deleteRoom(request,pk):
#     room=Room.objects.get(id=pk)
#     room.delete()
#     return redirect('home')


def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'home/delete.html',{'obj':room})