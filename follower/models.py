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
    follwers_list = FollowList.objects.get(user=removee)
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
      sender_follow_list = FollowList.objects.get(user=self.sender)
      if sender_follow_list:
        sender_follow_list.add_follower(self.reciever)
        self.is_active = True

  def decline(self):
    self.is_active = False
    self.save()

  def cancel(self):
    self.is_active = False
    self.save()
