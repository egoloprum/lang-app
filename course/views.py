from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from django.db import IntegrityError
from .models import *

def createCourse(request):
  host = request.user
  course = Course.objects.create(host=host)
  return redirect('course-edit', course.id)

def editCourse(request, pk):
  course = Course.objects.get(id=pk)
  contents = Content.objects.filter(course=course)
  topics = Topic.objects.all()
  tags = Tag.objects.all()
  context = {
    'course': course,
    'contents': contents,
    'topics': topics,
    'tags': tags,
  }
  if request.method == 'POST':
    name = request.POST.get('course-name')
    topic = request.POST.get('course-topic')
    tag = request.POST.get('course-tag')
    body = request.POST.get('course-body')
    start = request.POST.get('course-start')
    end = request.POST.get('course-end')

    course.name = name
    course.body = body
    course.start_date = start
    course.end_date = end
    course.publication = True
    course.save()

    return redirect('course')

  return render(request, 'course-edit.html', context)

def eachCourse(request, pk):
  course = Course.objects.get(id=pk)
  contents = Content.objects.filter(course=course)
  context = {
    'course': course,
    'contents': contents,
  }
  return render(request, 'course-each.html', context)

def course(request):
    topics = Topic.objects.all()
    courses = Course.objects.all()

    if request.method == 'POST':
      course_id = request.POST.get('course-delete')
      course = courses.get(id=course_id)
      course.delete()
      return redirect('course')   

    context = {'topics': topics, 'courses': courses}

    return render(request, 'course.html', context)

# def courseEach(request, pk):
#   course = Course.objects.get(id=pk)

#   if request.method == 'POST':
#     course.delete()
#     return redirect('course')

#   contents = Content.objects.select_related('course').filter(course=course)

#   if contents:
#     context = {'course': course, 'contents':contents}
#   else:
#     contents = None
#     context = {'course': course, 'contents':contents}

#   return render(request, 'course-each.html')

# def createCourse(request):
#     host = request.user
#     all_topic = Topic.objects.all()
#     course_form = CourseForm()

#     if request.method == "POST":
#         topic_html = request.POST.get('topic')
#         name = request.POST.get('name')
#         body = request.POST.get('body')
#         max_user_num = request.POST.get('max_user_num')

#         if Topic.objects.filter(name=topic_html):
#           topic = Topic.objects.get(name=topic_html)
#         else:
#           topic = Topic.objects.create(name=topic_html)

#         # topic, created = Topic.objects.get_or_create(name=topic_html)
#         if topic:
#           if max_user_num:
#             Course.objects.create(topic=topic, name=name, body=body, host=host, max_user_num=max_user_num)
#             return redirect('course')

#           try:
#             Course.objects.create(topic=topic, name=name, body=body, host=host)
#           except IntegrityError:
#              messages.error(request, "This name is already in use")
#              return redirect('create-course')
          
#           return redirect('course')
        
#         else:
#           topic = Topic.objects.create(name=topic_html)
#           Course.objects.get_or_create(topic=topic, name=name, body=body, host=host)
#           return redirect('course')

#     context = {'topics': all_topic, 'form': course_form}
#     return render(request, 'create-course.html', context)


def eachChapter(request, pk):
   content = Content.objects.get(id=pk)
   course = Course.objects.get(id=content.course.id)
   contents = Content.objects.filter(course=course)

   context = {'content': content, 'course': course, 'contents': contents}
   return render(request, 'content-each.html', context)   

def createChapter(request, pk):
  course = Course.objects.get(id=pk)
  content = Content.objects.create(course=course)
  return redirect('chapter-edit', course.id, content.id)

def editChapter(request, id, pk):
  content = Content.objects.get(id=id)
  course = Course.objects.get(id=pk)

  context = {
    'content': content,
    'course': course,
  }

  if request.method == "POST":
    name = request.POST.get('content-name')
    body = request.POST.get('content-body')
    content.name = name
    content.body = body
    content.save()
    return HttpResponse('<script type="text/javascript">window.close();</script>')

  return render(request, 'content-edit.html', context)

def createQuizFromCourse(request, pk):
  pass

def editQuizFromCourse(request, pk):
  pass

def createQuizFromChapter(request, pk):
  pass

def editQuizFromChapter(request, pk):
  pass

# def courseEachEdit(request, pk):
#    course = Course.objects.get(id=pk)
#    contents = Content.objects.filter(course=course)
#    content_name = []
#    content_body = []
#    num = Content.objects.filter(course=course).count()

#    if request.method == 'POST':

#       for content in contents:
#         content_name.append(request.POST.get('content-name-' + str(content.id)))
#         content_body.append(request.POST.get('content-body-' + str(content.id)))         

#       name = request.POST.get('name')
#       body = request.POST.get('body')
#       max_user_num = request.POST.get('max_user_num')

#       if max_user_num:
#           course.name = name
#           course.body = body
#           course.max_user_num = max_user_num
#           course.save()

#           x = 0
#           for content in contents:
#             content.name = content_name[x]
#             content.body = content_body[x]
#             content.save()
#             x += 1
          
#           return redirect('/course/each/%d'%course.id)

#       course.name = name
#       course.body = body
#       course.save()

#       x = 0
#       for content in contents:
#         content.name = content_name[x]
#         content.body = content_body[x]
#         content.save()
#         x += 1

#       return redirect('/course/each/%d'%course.id)

#    context = {'course': course, 'contents': contents}

#    return render(request, 'course-each-edit.html', context)

def topic(request, pk):
  topic = Topic.objects.get(id=pk)
  courses = Course.objects.select_related('topic').filter(topic=topic)

  context = {'courses':courses }

  return render(request, 'topic.html', context)

