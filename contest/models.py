from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Contest(models.Model):
  host = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
  user = models.ManyToManyField(User, related_name='contest_user', blank=True)

  name = models.CharField(max_length=200, unique=True, null=True, blank=True)
  body = models.TextField(null=True, blank=True)
  pts = models.IntegerField(default=0, null=True, blank=True)
  exp = models.IntegerField(default=0, null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  start_date = models.DateTimeField(null=True, blank=True)
  end_date = models.DateTimeField(null=True, blank=True)
  publication = models.BooleanField(default=False)


