import json
import asyncio
import time

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async

from follower.models import ChatRoom, Message
from django.contrib.auth.models import User 

class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.room_name = self.scope["url_route"]["kwargs"]
    self.room_group_name = f"chat_{self.room_name['pk']}"

    await (self.channel_layer.group_add)(
      self.room_group_name, self.channel_name
    )

    await self.accept()

  async def disconnect(self, close_code):
    await (self.channel_layer.group_discard)(
      self.room_group_name, self.channel_name
    )

  async def receive(self, text_data):
    text_data_json = json.loads(text_data)
    message = text_data_json["message"]
    username = text_data_json["username"]
    room = text_data_json["room"]

    if not message == '':
      await (self.save_message(message, username, room))

    await self.channel_layer.group_send(
      self.room_group_name,
      {
        "type": 'chat_message',
        "message": message,
        "username": username,
        "room": room,
      }
    )

  async def chat_message(self, event):
    message = event['message']
    username = event['username']
    room = event['room']

    await self.send(text_data=json.dumps({
      "message": message,
      "username": username,
      "room": room,
    }))

    print("data recieved")

  @sync_to_async
  def save_message(self, message, username, room):
    user = User.objects.get(username=username)
    room = ChatRoom.objects.get(id=room)

    Message.objects.create(user=user, room=room, body=message)

    print("message saved")
