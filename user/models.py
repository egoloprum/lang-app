from django.db import models
from django.contrib.auth.models import User

class Badge(models.Model):
  name = models.CharField(max_length=200, null=False)
  description = models.CharField(max_length=500, null=True)
  picture = models.ImageField(null=False)

  def __str__(self):
    return self.name

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
  badges = models.ManyToManyField(Badge, blank=True)

  birthday = models.DateTimeField(null=True, blank=True)
  level = models.SmallIntegerField(null=False, default=1)
  gender = models.CharField(max_length=100, blank=True, null=True)
  country = models.CharField(max_length=100, blank=True, null=True)
  active = models.BooleanField(default=False, null=True, blank=True)
  avatar = models.ImageField(blank=True, default="photos/pic.jpg", upload_to="photos/")

  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user.username
  
