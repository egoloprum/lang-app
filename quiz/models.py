from django.db import models
from django.contrib.auth.models import User
import random
# Create your models here.

class Quiz(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    number_of_questions = models.IntegerField()
    duration = models.TimeField(help_text="duration of the quiz in minutes")
    required_score = models.IntegerField(help_text="required score in %")
    difficulty = models.CharField(max_length=50)

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

class Question(models.Model):
    body = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
    
    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    body = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.body

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)
