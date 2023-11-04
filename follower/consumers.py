import json
import asyncio
import time

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async

from django.db.models import Count
from follower.models import ChatRoom, Message, NotificationList, Notification
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

    print("chat data recieved")

  @sync_to_async
  def save_message(self, message, username, room):
    user = User.objects.get(username=username)
    room = ChatRoom.objects.get(id=room)

    Message.objects.create(user=user, room=room, body=message)
    print("chat message saved")


# notification consumer
class NotificationConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.group_name = 'notification'

    await (self.channel_layer.group_add)(
      self.group_name, self.channel_name
    )

    await self.accept()

  async def disconnect(self, close_code):
    await (self.channel_layer.group_discard)(
      self.group_name, self.channel_name
    )

  async def receive(self, text_data):
    text_data_json = json.loads(text_data)
    type_data = text_data_json["type_data"]

    if type_data == 'course-edit':
      notif_body = text_data_json["notif_body"]
      notif_user = text_data_json["course_host"]
      notif_course = text_data_json["course_name"]
      request_user = text_data_json["request_user"]

      if not notif_body == '':
        await (self.save_notif(notif_body, notif_user))

      await self.channel_layer.group_send(
        self.group_name,
        {
          "type": 'notif_message',
          "type_data": type_data,
          "notif_body": notif_body,
          "notif_user": notif_user,
          "notif_course": notif_course,
          'request_user': request_user,
        }
      )

  async def notif_message(self, event):
    type_data = event['type_data']
    notif_body = event['notif_body']
    notif_user = event['notif_user']
    notif_course = event['notif_course']
    request_user = event['request_user']

    notif_count = await (self.notif_counter(request_user))
    print(notif_count)

    if type_data == 'course-edit':
      await self.send(text_data=json.dumps({
        "notif_body": notif_body,
        "notif_user": notif_user,
        "notif_course": notif_course,
        "notif_count": notif_count,
      }))

  @sync_to_async
  def save_notif(self, notif_body, notif_user):
    user = User.objects.get(username=notif_user)
    notification = Notification.objects.create(user=user, body=notif_body)
    for list in NotificationList.objects.all():
      list.notification.add(notification)
      
    print("notification saved")

  @sync_to_async
  def notif_counter(self, username):
    user = User.objects.get(username=username)
    list = NotificationList.objects.get(user=user)

    return list.notification.all().count()
