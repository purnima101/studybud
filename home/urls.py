from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.home,name="home"),
    path('room/<str:pk>/', views.room,name="room"),
    path('room_form/', views.createRoom,name="room_form"),
    path('update_room/<str:pk>', views.updateRoom,name="update_room"),
   
    path('delete_room/<str:pk>', views.deleteRoom,name="delete_room"),
    # path('topicpage/', views.topicpage,name="topicpage"),
]
