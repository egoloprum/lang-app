import json
import random
from django.shortcuts import render, redirect
from itertools import chain

from django.contrib.auth.models import User
from course.models import Course
from quiz.models import Quiz
from follower.models import NotificationList

# Create your views here.

def home(request):
    courses = Course.objects.select_related('host').order_by('-start_date')[:5]
    quizs = Quiz.objects.prefetch_related('question_quiz').select_related('host').order_by('-start_date')[:5]
    users = User.objects.select_related('profile').filter(is_staff=False).order_by('?')
    staffs = User.objects.select_related('profile').filter(is_staff=True).order_by('?')
    users_count = users.count()
    staffs_count = staffs.count()

    list_count = 0

    if request.user.is_authenticated:
        list_count = NotificationList.objects.get(user=request.user).notification.all().count()

    elements = set(chain(courses, quizs))
    context = {
        'courses': courses,
        'quizs': quizs,
        'elements': elements,
        'list_count': list_count,
        'users': users.exclude(id=request.user.id)[:20],
        'staffs': staffs.exclude(id=request.user.id)[:20],
        'users_count': users_count,
        'staffs_count': staffs_count,
    }
    return render(request, 'index.html', context)

def calendar(request):
    list_count = NotificationList.objects.get(user=request.user).notification.all().count()

    context = {
        'list_count': list_count,
    }

    return render(request, 'calendar.html', context)




