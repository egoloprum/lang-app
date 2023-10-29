from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
  name = models.CharField(unique=True, null=False, max_length=200)

  def __str__(self):
    if self.name == None:
      return f" {self.id} empty"
    else:
      return f" {self.id} {self.name}"

TAG_CHOICES = (
  ('Beginner', 'beginner'),
  ('Intermediate', 'intermediate'),
  ('Advanced', 'advanced'),
)

class Course(models.Model):
  host = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='course_host')
  user = models.ManyToManyField(User, blank=True, related_name='course_user')
  topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True, related_name='course_topic')
  tag = models.CharField(max_length=50, choices=TAG_CHOICES, default=None, null=True, blank=True)
  
  # if all quizs of it is completed 
  # completion = models.ManyToManyField(Completion)

  name = models.CharField(unique=True, max_length=200, null=True)
  body = models.TextField(null=True, blank=True) 
  pts = models.IntegerField(default=0, null=True, blank=True)
  exp = models.IntegerField(default=0, null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  start_date = models.DateTimeField(null=True, blank=True)
  end_date = models.DateTimeField(null=True, blank=True) 
  publication = models.BooleanField(default=False) 

  def __str__(self):
    if self.name == None:
      return f" {self.id} empty"
    else:
      return f" {self.id} {self.name}"

  def get_quiz_count(self):
    try:
     return self.quiz_set.all().count
    except models.FieldDoesNotExist:
      return 0

class Content(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, related_name='content_course')

  name = models.CharField(max_length=200, null=True)
  body = models.TextField(null=True, blank=True)
  publication = models.BooleanField(default=False)
  
  def __str__(self):
    if self.name == None:
      return f" {self.id} empty"
    else:
      return f" {self.id} {self.name}"

class File(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='file_course')
  content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True, related_name='file_content')
  
  file = models.FileField(null=False, upload_to='files/')
  description = models.CharField(max_length=200, null=False)

  def __str__(self):
    if self.description == None:
      return f" {self.id} empty"
    else:
      return f" {self.id} {self.description}"
    
class Progress(models.Model):
  user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='progress_user')
  course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE, related_name='progress_course')

  value = models.FloatField(default=0, null=False, blank=False)
