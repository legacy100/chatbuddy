from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
# pass in a dynamic url routing with the <str:pk>
    path('room/<str:pk>/', views.room, name='room'),

    path('chat-room/', views.createChat, name='chat-room'),
]