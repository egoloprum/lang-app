from django.db import models
from django.contrib.auth.models import User
import random
from course.models import Course, Content
# Create your models here.

class Quiz(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_host')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quiz_course', null=True, blank=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='quiz_content', null=True, blank=True)

    pts = models.IntegerField(default=0, null=True, blank=True)
    exp = models.IntegerField(default=0, null=True, blank=True)

    name = models.CharField(max_length=200, null=True, blank=True)
    duration = models.TimeField(help_text="duration of the quiz in minutes", null=True, blank=True)
    required_score = models.IntegerField(help_text="required score in %", default=60, null=True, blank=True)
    difficulty = models.CharField(max_length=50, null=True, blank=True)
    publication = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.course:
            return f" {self.id} {self.name} in course ({ self.course.name })"
        elif self.content:
            return f" {self.id} {self.name} in content ({ self.content.name } of {self.content.course.name})"
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
        return f"id==({ self.id }) quiz==({ self.quiz.name }) // ({self.body})"
    
    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    body = models.CharField(max_length=200, null=False)
    correct = models.BooleanField(default=False, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, related_name='answer_question')

    def __str__(self):
        return f"id==({self.id}) question==({self.question.id}) // ({self.body})"

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=False, related_name='result_quiz')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='result_user')

    has_course = models.BooleanField(null=True, blank=True)
    has_content = models.BooleanField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"quiz==({ self.quiz.name }) user==({ self.user.username }) score==({ self.score })"

class Selected_Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='sel_answer_user')
    selected = models.ForeignKey(Answer, on_delete=models.CASCADE, null=False, related_name='sel_answer_ans')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, related_name='sel_answer_ques')
    result = models.ForeignKey(Result, on_delete=models.CASCADE, null=False, related_name='sel_answer_result')

    def __str__(self):
        return f"question==({ self.question.id }) user==({ self.user.username }) answer==({ self.selected.id })"

class Average_score(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, related_name='average_score_quiz')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, related_name='average_score_ques')
    user = models.ManyToManyField(User, related_name='average_score_user')
    score = models.FloatField()

    def __str__(self):
        return f"quiz==({ self.quiz.name }) user==({ self.user.username }) score==({ self.score })"

