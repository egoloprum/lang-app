from django.db import models
from django.contrib.auth.models import User
import random
from course.models import Course, Content
from contest.models import Contest
# Create your models here.

class Quiz(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_host')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quiz_course', null=True, blank=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='quiz_content', null=True, blank=True)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='quiz_contest', null=True, blank=True)

    pts = models.IntegerField(default=0, null=True, blank=True)
    exp = models.IntegerField(default=0, null=True, blank=True)

    name = models.CharField(max_length=200, null=True, blank=True)
    duration = models.TimeField(help_text="duration of the quiz in minutes", null=True, blank=True)
    required_score = models.IntegerField(help_text="required score in %", null=True, blank=True)
    difficulty = models.CharField(max_length=50, null=True, blank=True)
    publication = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)  

    def __str__(self):
        if self.name == None:
            return f" {self.id} empty"
        else:
            return f" {self.id} {self.name}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.len(questions)]

class Question(models.Model):
    body = models.CharField(max_length=200, null=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=False, related_name='question_quiz')
    explanation = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        if self.body == None:
            return f" {self.id} empty"
        else:
            return f" {self.id} / {self.body}"
    
    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    body = models.CharField(max_length=200, null=False)
    correct = models.BooleanField(default=False, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, related_name='answer_question')

    def __str__(self):
        if self.body == None:
            return f" {self.id} empty"
        else:
            return f"{self.question.id} / {self.id} / {self.body}"

class Selected_Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='sel_answer_user')
    selected = models.ForeignKey(Answer, on_delete=models.CASCADE, null=False, related_name='sel_answer_ans')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, related_name='sel_answer_ques')

    def __str__(self):
        if self == None:
            return f"{self.id} empty"
        else:
            return f"{self.selected.id} / {self.id}"

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=False, related_name='result_quiz')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='result_user')
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

class Average_score(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, related_name='average_score_quiz')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, related_name='average_score_ques')
    user = models.ManyToManyField(User, related_name='average_score_user')
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)

