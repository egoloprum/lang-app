from django.db import models
from django.contrib.auth.models import User
import random
from course.models import Course, Content
# Create your models here.

class Quiz(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_host')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quiz_course', null=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='quiz_content', null=True)

    # when entering url function which rendered from views makes this variable false 
    # completed -1, 0, 1
    # if -1 never started and accomplished
    # if 0 started but never accomplished
    # if 1 accomplished
    completed = models.SmallIntegerField(default=-1, null=False)
    name = models.CharField(max_length=200, null=False)
    duration = models.TimeField(help_text="duration of the quiz in minutes", null=True, blank=True)
    required_score = models.IntegerField(help_text="required score in %", null=True, blank=True)
    difficulty = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.len(questions)]

class Question(models.Model):
    body = models.CharField(max_length=200, null=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=False, related_name='question_quiz')
    explanation = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.body
    
    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    body = models.CharField(max_length=200, null=False)
    correct = models.BooleanField(default=False, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)

    def __str__(self):
      return self.body

class Selected_Answer(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False, null=False)


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    selected_answer = models.ForeignKey(Selected_Answer, on_delete=models.CASCADE, null=True)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

class Average_score(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, related_name='average_score_quiz')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    score = models.FloatField()

