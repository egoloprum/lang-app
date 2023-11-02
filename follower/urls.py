from django.urls import path
from . import views

urlpatterns = [
  path('<str:pk>/', views.followerList, name='followers'),
  path('<str:pk>/send_follow_request', views.send_follow_request, name='send-follow-request'),
  path('<str:pk>/accept_follow_request', views.accept_follow_request, name='accept-follow-request'),
  path('<str:pk>/decline_follow', views.decline_follow, name='decline-follow'),
  # FROM REQUEST USER SIDE
  path('<str:pk>/cancel_follow_request', views.cancel_follow_request, name='cancel-follow-request'),
  # FROM RECIEVER SIDE
  path('<str:pk>/cancel_request', views.cancel_request, name='cancel-request'),

  path('chats', views.chatRoom, name='chatroom'),
  path('chats/<str:pk>', views.eachChat, name='chat-each'),
  path('chat-create', views.createChatroom, name='create-chatroom'),
]
