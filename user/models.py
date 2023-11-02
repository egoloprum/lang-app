from django.db import models
from django.contrib.auth.models import User
from quiz.models import Quiz
from course.models import Course, Content

class Badge(models.Model):
  host = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=200, null=False)
  description = models.CharField(max_length=500, null=True, blank=True)
  picture = models.ImageField(null=True, blank=True, upload_to='badges/')
  pts = models.IntegerField(default=0, null=True, blank=True)
  exp = models.IntegerField(default=0, null=True, blank=True)

  def __str__(self):
    return self.name

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
  badge = models.ManyToManyField(Badge, blank=True)
  points = models.IntegerField(default=0, null=False)
  experience = models.IntegerField(default=0, null=False)

  birthday = models.DateTimeField(null=True, blank=True)
  level = models.SmallIntegerField(null=False, default=1)
  gender = models.CharField(max_length=100, blank=True, null=True)
  country = models.CharField(max_length=100, blank=True, null=True)
  # active now feature
  active = models.BooleanField(default=False, null=True, blank=True)
  avatar = models.ImageField(blank=True, default="photos/pic.jpg", upload_to="photos/")

  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user.username
  
class Completion(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True, related_name='completion_quiz')
  course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
  content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True)
  completed = models.BooleanField(default=False)  

  def __str__(self):
    return f"user==({ 'none' if self.user == None else self.user.username }) quiz==({ 'none' if self.quiz == None else self.quiz.name }) course==({ 'none' if self.course == None else self.course.name }) content==({ 'none' if self.content == None else self.content.name })"
