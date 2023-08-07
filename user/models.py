from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Gender(models.Model):
  name = models.CharField(max_length=200, null=True)

  def __str__(self):
    return self.name

class Badge(models.Model):
  name = models.CharField(max_length=200, null=False)
  description = models.CharField(max_length=500, null=True)
  picture = models.ImageField(null=False)

  def __str__(self):
    return self.name

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
  gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)

  birthday = models.DateTimeField(null=True)
  level = models.SmallIntegerField(null=False, default=1)
  updated_at = models.DateTimeField(auto_now=True)
  avatar = models.ImageField(blank=True, default="images/avatar.png")

  def __str__(self):
    return self.user.username
  
