from itertools import count
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


# Create your views here.



# rooms=[
#     {'id':1,'name':'Purnima'},
#     {'id':2,'name':'Yatin'},
#     {'id':3,'name':'Irfan'},

# ]


def login_regis(request):
    page='login'
    
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, 'User doesnt exit!!!')

        user=authenticate(request,username=username,password=password)
        if user!=None:
            login(request,user)
            return redirect('home')
            
        else:
            messages.error(request, 'Wrong Password')

    context={'page':page}
    return render(request,'home/login_regis.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def register(request):
    page='register'
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Try again')
            return redirect('home')


    context={'page':page,'form':form}
    return render(request,'home/login_regis.html',context)

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
    if request.method=="POST":
        message=request.POST.get('message')
        Message.objects.create(user=request.user,room=room,body=message)
        return redirect('room',pk=room.id)
    



    messages=room.message_set.all().order_by('-created')
    context={'room':room,'messages':messages}
    return render(request,'home/room.html',context)


@login_required(login_url='login_regis')
def createRoom(request):
    form=RoomForm()
    if request.method=="POST":
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'home/room_form.html',context)


@login_required(login_url='login_regis')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("Not allowed!")
        

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

@login_required(login_url='login_regis')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("Not allowed!")
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'home/delete.html',{'obj':room})



