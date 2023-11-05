import json
from django.shortcuts import render, redirect
from itertools import chain

from course.models import Course
from quiz.models import Quiz
from follower.models import NotificationList

# Create your views here.

def home(request):
    courses = Course.objects.select_related('host').order_by('-start_date')[:5]
    quizs = Quiz.objects.select_related('host').order_by('-start_date')[:5]

    list_count = NotificationList.objects.get(user=request.user).notification.all().count()

    elements = set(chain(courses, quizs))

    context = {
        'courses': courses,
        'quizs': quizs,
        'elements': elements,
        'list_count': list_count,
    }
    return render(request, 'index.html', context)

def calendar(request):
    list_count = NotificationList.objects.get(user=request.user).notification.all().count()

    context = {
        'list_count': list_count,
    }

    return render(request, 'calendar.html', context)




