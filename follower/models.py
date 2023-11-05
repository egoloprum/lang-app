from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class FollowList(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
  followers = models.ManyToManyField(User, blank=True, related_name='followers')

  def __str__(self):
    return self.user.username
  
  def add_follower(self, account):
    if not account in self.followers.all():
      self.followers.add(account)

  def remove_follower(self, account):
    if account in self.followers.all():
      self.followers.remove(account)

  def unfollow(self, removee):
    remover_followers_list = self
    remover_followers_list.remove_follower(removee)
    try:
      follwers_list = FollowList.objects.get(user=removee)
    except:
      follwers_list = FollowList.objects.create(user=removee)
    follwers_list.remove_follower(self.user)

  def is_mutual_follower(self, follower):
    if follower in self.followers.all():
      return True
    
    return False
  

class FollowRequest(models.Model):
  sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
  reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever')

  is_active = models.BooleanField(blank=True, null=False, default=True)
  timestamp = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.sender.username

  def accept(self):
    reciever_follow_list = FollowList.objects.get(user=self.reciever)
    if reciever_follow_list:
      reciever_follow_list.add_follower(self.sender)
      try:
        sender_follow_list = FollowList.objects.get(user=self.sender)
      except FollowList.DoesNotExist:
        sender_follow_list = FollowList.objects.create(user=self.sender)

      if sender_follow_list:
        sender_follow_list.add_follower(self.reciever)
        self.is_active = True

  def decline(self):
    self.is_active = False
    self.save()

  def cancel(self):
    self.is_active = False
    self.save()


class ChatRoom(models.Model):
  host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatroom_host')
  user = models.ManyToManyField(User, related_name='chatroom_user', blank=True)
  name = models.CharField(max_length=200, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

class Message(models.Model):
  room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='message_chatroom')
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_user')

  body = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.body} by {self.user.username} in {self.room.name}"

class Notification(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notif_sender')
  body = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  is_read = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.user} has recieved {self.body}"

class NotificationList(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='list_user')
  notification = models.ManyToManyField(Notification, related_name='list_notification')

  def __str__(self):
    return f"{self.user.username}"
