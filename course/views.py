from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

from django.db import IntegrityError

from .models import *

def createCourse(request):
    host = request.user
    all_topic = Topic.objects.all()

    if request.method == "POST":
        topic_html = request.POST.get('topic')
        name = request.POST.get('name')
        body = request.POST.get('body')
        max_user_num = request.POST.get('max_user_num')

        if Topic.objects.filter(name=topic_html):
          topic = Topic.objects.get(name=topic_html)
        else:
          topic = Topic.objects.create(name=topic_html)

        # topic, created = Topic.objects.get_or_create(name=topic_html)

        if topic:
          if max_user_num:
            Course.objects.create(topic=topic, name=name, body=body, host=host, max_user_num=max_user_num)
            return redirect('course')

          try:
            Course.objects.create(topic=topic, name=name, body=body, host=host)
          except IntegrityError:
             messages.error(request, "This name is already in use")
             return redirect('create-course')
          
          return redirect('course')
        
        else:
          topic = Topic.objects.create(name=topic_html)
          Course.objects.get_or_create(topic=topic, name=name, body=body, host=host)
          return redirect('course')

        

    context = {'topics': all_topic}

    return render(request, 'create-course.html', context)

def course(request):
    topics = Topic.objects.all()
    courses = Course.objects.all()

    context = {'topics': topics, 'courses': courses}

    return render(request, 'course.html', context)

def courseEach(request, pk):
  course = Course.objects.get(id=pk)
  contents = None
  contents = Content.objects.filter(course=course)

  if Content.objects.filter(course=course):
    contents = Content.objects.filter(course=course)
    context = {'course': course, 'contents':contents}
  else:
    context = {'course': course, 'contents':contents}

  return render(request, 'course-each.html', context)

def courseEachContent(request):
  if request.method == 'POST':
    name = request.POST.get('name')
    body = request.POST.get('body')
    course_id = request.POST.get('course-id')

    Content.objects.get_or_create(name=name, body=body, course=course)

    messages.success(request, 'Content has been created')
    return HttpResponse('success !')
   

def courseEachEdit(request, pk):
   course = Course.objects.get(id=pk)

   if request.method == 'POST':
      name = request.POST.get('name')
      body = request.POST.get('body')
      max_user_num = request.POST.get('max_user_num')

      if max_user_num:
          course.name = name
          course.body = body
          course.max_user_num = max_user_num
          course.save()

          return redirect('/course/each/%d'%course.id)

      course.name = name
      course.body = body
      course.save()
      return redirect('/course/each/%d'%course.id)

      

   context = {'course': course}

   return render(request, 'course-each-edit.html', context)

def topic(request, pk):
  topic = Topic.objects.get(id=pk)
  courses = Course.objects.filter(topic=topic)

  context = {'courses':courses }

  return render(request, 'topic.html', context)

