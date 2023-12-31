from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/follower/chats/<str:pk>/', consumers.ChatConsumer.as_asgi()),
    path('ws/follower/notifications', consumers.NotificationConsumer.as_asgi()),
]
