from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
  name = models.CharField(unique=True, null=False, max_length=200)

  def __str__(self):
    return self.name
  
class File(models.Model):
  file = models.FileField(null=True)
  file_description = models.CharField(max_length=200, null=True)

  def __str__(self):
    return self.file_description

class Course(models.Model):
  host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  user = models.ManyToManyField(User, related_name='course_user', blank=True)
  topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=False, related_name='course_topic')
  
  # if all quizs of it is completed 
  completed = models.BooleanField(default=False, null=False)
  max_user_num = models.IntegerField(null=True)
  name = models.CharField(unique=True, max_length=200, null=False)
  body = models.TextField(null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name

  def get_quiz_count(self):
    try:
     return self.quiz_set.all().count
    except models.FieldDoesNotExist:
      return 0

class Content(models.Model):
  name = models.CharField(max_length=200, null=False)
  body = models.TextField(null=False)
  files = models.ForeignKey(File, on_delete=models.CASCADE, null=True)
  course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, related_name='content_course')

  def __str__(self):
    return self.name
