from django.db import models
from django.contrib.auth.models import User

from .validators import validate_file_size

TAG_CHOICES = (
  ('Beginner', 'beginner'),
  ('Intermediate', 'intermediate'),
  ('Advanced', 'advanced'),
)

TOPIC_CHOICES = (
  ('Advice', 'advice'),
  ('Development', 'development'),
)

class Course(models.Model):
  host = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='course_host')
  user = models.ManyToManyField(User, blank=True, related_name='course_user')
  
  topic = models.CharField(max_length=50, choices=TAG_CHOICES, default=None, null=True, blank=True)
  tag = models.CharField(max_length=50, choices=TOPIC_CHOICES, default=None, null=True, blank=True)
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
      return f"host==({ self.host.username }) name==({ self.name })"

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
    return f"course==({ self.course.name }) name==({ self.name })"

class File(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='file_course')
  content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True, related_name='file_content')
  
  file = models.FileField(null=False, upload_to='files/', validators=[validate_file_size])
  description = models.CharField(max_length=200, null=False)

  def __str__(self):
    if self.course:
      return f"course==({ self.course.name }) id==({ self.id })"
    elif self.content:
      return f"content==({ self.content.id }) id==({ self.id })"
    else:
      return f"id==({ self.id })"
    
class Progress(models.Model):
  user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='progress_user')
  course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE, related_name='progress_course')

  value = models.FloatField(default=0, null=False, blank=False)

  def __str__(self):
    return f"course=={ self.course.name } user=={ self.user.username } value=={ self.value }"
