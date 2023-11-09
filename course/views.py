import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q

from .models import *
from quiz.models import Quiz
from user.models import Completion, Profile, Badge
from follower.models import NotificationList

@login_required(login_url='login')
def createCourse(request):
  host = request.user
  course = Course.objects.create(host=host)
  course.name = f"Course {course.id}"
  course.save()
  return redirect('course-edit', course.id)

@login_required(login_url='login')
def course(request):
  topics = Topic.objects.all()
  list_count = NotificationList.objects.get(user=request.user).notification.all().count()

  context = {}
  context['topics'] = topics
  context['list_count'] = list_count

  courses = Course.objects.select_related('host').order_by('-created_at')
  course_progresses = []

  if request.user.is_staff:
    for course in courses:
      course_progresses.append('course')

    course_progresses = zip(courses, course_progresses)
    context['course_progresses'] = course_progresses

  else:
    courses = courses.filter(publication=True)
    for course in courses:
      try:
        progress = Progress.objects.get(course=course, user=request.user)
      except Progress.DoesNotExist:
        progress = 'course'
      course_progresses.append(progress)

      if not progress == 'course' and progress.value == 100.0:
        try:
          course_completed = Completion.objects.get(course=course, user=request.user, content=None, quiz=None)
        except Completion.DoesNotExist:
          course_completed = Completion.objects.create(course=course, user=request.user, content=None, quiz=None)

        course_completed.completed = True
        course_completed.save()

    courses_completion = Completion.objects.select_related('course').filter(completed=True, user=request.user, content=None, quiz=None).count()
    print(courses_completion)

    course_progresses = zip(courses, course_progresses)
    context['course_progresses'] = course_progresses

  return render(request, 'course.html', context)

def searchCourse(request):
  search_tag = request.POST.get('course-tags')
  search_date = request.POST.get('course-date')
  search_name = request.POST.get('course-search')

  course_progresses = []
  context = {}

  current_time = datetime.datetime.now()
  courses = Course.objects.select_related('host').order_by('-created_at')

  courses = courses.filter(Q(name__icontains=search_name))

  if search_tag == 'Beginner':
    courses = courses.filter(Q(tag=search_tag))
  elif search_tag == 'Intermediate':
    courses = courses.filter(Q(tag=search_tag))
  elif search_tag == 'Advanced':
    courses = courses.filter(Q(tag=search_tag))

  if search_date == 'Started':
    courses = courses.filter(Q(start_date__lte=current_time))
  elif search_date == 'Ended':
    courses = courses.filter(Q(end_date__lte=current_time))
  elif search_date == 'Not yet':
    courses = courses.filter(Q(start_date__gte=current_time))

  if request.user.is_staff:
    for course in courses:
      course_progresses.append('course')

    course_progresses = zip(courses, course_progresses)
    context['course_progresses'] = course_progresses

  else:
    courses = courses.filter(publication=True)
    for course in courses:
      try:
        progress = Progress.objects.get(course=course, user=request.user)
      except Progress.DoesNotExist:
        progress = ''
      course_progresses.append(progress)

    course_progresses = zip(courses, course_progresses)
    context['course_progresses'] = course_progresses

  return render(request, 'course-partial.html', context)

@login_required(login_url='login')
def editCourse(request, pk):
  course = Course.objects.select_related('host').get(id=pk)
  quizs = Quiz.objects.select_related('course').filter(course=course).annotate(questions_count=models.Count('question_quiz'))
  contents = Content.objects.select_related('course').filter(course=course)
  contents = contents.annotate(quizs_count=models.Count('quiz_content'), files_count=models.Count('file_content'))
  topics = Topic.objects.all()

  if request.method == 'POST':
    name = None if request.POST.get('course-name') == '' else request.POST.get('course-name')
    topic = None if request.POST.get('course-topic') == '' else request.POST.get('course-topic')
    tag = None if request.POST.get('course-tag') == '' else request.POST.get('course-tag')
    body = None if request.POST.get('course-body') == '' else request.POST.get('course-body')
    start = None if request.POST.get('course-start') == '' else request.POST.get('course-start')
    end = None if request.POST.get('course-end') == '' else request.POST.get('course-end')
    public = True if request.POST.get('course-public') == 'on' else False

    course.name = name
    course.body = body
    course.start_date = start
    course.end_date = end
    course.publication = public

    x = 1
    files = []

    while(request.POST.get('cour-file-desc-' + str(x))):
      file_desc = request.POST.get('cour-file-desc-' + str(x))
      file = request.POST.get('cour-file-' + str(x))
      files.append(File.objects.create(file=file, description=file_desc, course=course))
      x += 1
  
    course.save()
    return redirect('course')

  course_files = File.objects.filter(course=course).select_related('course')
  content_files = []

  for content in contents:
    for file in File.objects.filter(content=content).select_related('content'):
      content_files.append(file)

  list_count = NotificationList.objects.get(user=request.user).notification.all().count()

  context = {
    'course': course,
    'quizs': quizs,
    'contents': contents,
    'topics': topics,
    'cour_files': course_files,
    'cont_files': content_files,
    'list_count': list_count,
  }

  return render(request, 'course-edit.html', context)

@login_required(login_url='login')
def deleteCourse(request, pk):
  course = Course.objects.get(id=pk)
  course.delete()
  return redirect('course')

@login_required(login_url='login')
def resultCourse(request, pk):
  course = Course.objects.select_related('host', 'topic').get(id=pk)
  contents = Content.objects.select_related('course').filter(course=course)
  files = File.objects.select_related('course').filter(course=course)
  quizs = Quiz.objects.select_related('course').filter(course=course)
  course_users = course.user.all()
  progresses = Progress.objects.select_related('course', 'user').filter(course=course)

  course_users = list(zip(course_users, progresses))
  list_count = NotificationList.objects.get(user=request.user).notification.all().count()

  context = {
    'course': course,
    'course_users': course_users,
    'contents': contents,
    'files': files,
    'quizs': quizs,
    'progresses': progresses,
    'list_count': list_count,
  }
  return render(request, 'course-result.html', context)

@login_required(login_url='login')
def eachCourse(request, pk):
  course = Course.objects.get(id=pk)
  course.user.add(request.user)
  contents = Content.objects.filter(course=course)
  quizs = Quiz.objects.select_related('course').filter(course=course)
  completion_quizs = []
  course_quiz_completed = 0
  contents_completed_count = 0

  try:
    Completion.objects.get(course=course, content=None, quiz=None, user=request.user)
  except Completion.DoesNotExist:
    Completion.objects.create(course=course, content=None, quiz=None, user=request.user)

  if not request.user.is_staff:
    for content in contents:
      content_quizs = Quiz.objects.select_related('content').filter(content=content)
      try:
        content_completion = Completion.objects.get(course=course, content=content, quiz=None, user=request.user)
      except Completion.DoesNotExist:
        content_completion = Completion.objects.create(course=course, content=content, quiz=None, user=request.user)

      content_quiz_completed = 0
      for quiz in content_quizs:
        try:
          content_quiz_completion = Completion.objects.get(course=course, content=content, quiz=quiz, user=request.user)
        except Completion.DoesNotExist:
          content_quiz_completion = Completion.objects.create(course=course, content=content, quiz=quiz, user=request.user)

        if content_quiz_completion.completed:
          content_quiz_completed += 1

      try:
        if content_quiz_completed / content_quizs.count() == 1:
          content_completion.completed = True
          content_completion.save()
          contents_completed_count += 1

      except ZeroDivisionError:
        print('content quizs is empty')

  print(content_completion) 
          
  for quiz in quizs:
    if not request.user.is_staff:
      try:
        course_quiz_completion = Completion.objects.get(course=course, content=None, quiz=quiz, user=request.user)

        if course_quiz_completion.completed:
          course_quiz_completed += 1

      except Completion.DoesNotExist:
        course_quiz_completion = Completion.objects.create(course=course, content=None, quiz=quiz, user=request.user)

      completion_quizs.append(course_quiz_completion)
    else:
      completion_quizs.append('completion')

  if not request.user.is_staff:
    try:
      progress = Progress.objects.get(user=request.user, course=course)
    except Progress.DoesNotExist:
      progress = Progress.objects.create(user=request.user, course=course)
      profile = Profile.objects.get(user=request.user)
      profile.badge.add(Badge.objects.get(name='Time to Study'))
      profile.save()

    course_elements = quizs.count() + contents.count()

    try:
      course_quizs_completed_count = quizs.count() / course_quiz_completed
    except ZeroDivisionError:
      course_quizs_completed_count = 0

    progress.value = (course_quizs_completed_count + contents_completed_count) / course_elements * 100
    progress.save()

    print(progress.value)
  
  files = File.objects.filter(course=course)
  completion_quizs = zip(quizs, completion_quizs)

  list_count = NotificationList.objects.get(user=request.user).notification.all().count()

  context = {
    'course': course,
    'contents': contents,
    'completion_quizs': completion_quizs,
    'files': files,
    'list_count': list_count,
  }
  return render(request, 'course-each.html', context)

@login_required(login_url='login')
def eachChapter(request, pk):
  content = Content.objects.select_related('course')

  this_content = content.get(id=pk)
  course = Course.objects.select_related('host').get(id=this_content.course.id)
  contents = content.filter(course=course)

  quizs = Quiz.objects.select_related('content').filter(content=this_content)

  completion_quizs = []
  for quiz in quizs:
    try:
      completion = Completion.objects.get(quiz=quiz, user=request.user)
    except Completion.DoesNotExist:
      completion = Completion.objects.create(quiz=quiz, user=request.user)

    completion_quizs.append(completion)

  completion_quizs = zip(quizs, completion_quizs)
  list_count = NotificationList.objects.get(user=request.user).notification.all().count()

  context = {
    'content': this_content, 
    'course': course, 
    'contents': contents,
    'completion_quizs': completion_quizs,
    'list_count': list_count
  }
  
  return render(request, 'content-each.html', context)   

@login_required(login_url='login')
def createChapter(request, pk):
  course = Course.objects.get(id=pk)
  try:
    content = Content.objects.create(course=course)
    content.name = "New chapter"
    content.save()
    return HttpResponse(content.id)
  except Content.DoesNotExist:
    return HttpResponse('Something is wrong')
  
@login_required(login_url='login')
def deleteChapter(request, pk):
  content = Content.objects.get(id=pk)
  try:
    content.delete()
    return HttpResponse('Chapter successfully deleted')
  except Exception:
    return HttpResponse('Something is wrong')

@login_required(login_url='login')
def editChapter(request, id, pk):
  content = Content.objects.get(id=id)
  course = Course.objects.get(id=pk)
  quizs = Quiz.objects.filter(content=content).annotate(questions_count=models.Count('question_quiz'))
  list_count = NotificationList.objects.get(user=request.user).notification.all().count()

  context = {
    'content': content,
    'course': course,
    'quizs': quizs,
    'list_count': list_count,
  }

  if request.method == "POST":
    name = request.POST.get('content-name')
    body = request.POST.get('content-body')
    public = True if request.POST.get('content-pub') == 'on' else False
    content.name = name
    content.body = body
    content.publication = public

    x = 1
    while(request.POST.get('chap-file-desc-' + str(x))):
      desc = request.POST.get('chap-file-desc-' + str(x))
      file = request.POST.get('chap-file-' + str(x))
      File.objects.create(content=content, description=desc, file=file)
      x += 1

    content.save()
    return HttpResponse('<script type="text/javascript">window.close();</script>')

  return render(request, 'content-edit.html', context)

@login_required(login_url='login')
def createQuizFromCourse(request, pk):
  course = Course.objects.get(id=pk)
  try:
    quiz = Quiz.objects.create(host=request.user, course=course)
    return HttpResponse(quiz.id)
  except Quiz.DoesNotExist:
    return HttpResponse('Something is wrong')
  
@login_required(login_url='login')
def deleteQuizFromCourse(request, pk):
  quiz = Quiz.objects.get(id=pk)
  try:
    quiz.delete()
    return HttpResponse('Quiz successfully deleted')
  except Quiz.DoesNotExist:
    return HttpResponse('Something is wrong')

@login_required(login_url='login')
def createQuizFromChapter(request, pk):
  content = Content.objects.get(id=pk)
  try:
    quiz = Quiz.objects.create(content=content, host=request.user)
    return HttpResponse(quiz.id)
  except Quiz.DoesNotExist:
    return HttpResponse("Something is wrong")

@login_required(login_url='login')
def deleteQuizFromChapter(request, pk):
  quiz = Quiz.objects.get(id=pk)
  try:
    quiz.delete()
    return HttpResponse('Quiz successfully deleted')
  except Exception:
    return HttpResponse('Something is wrong')

@login_required(login_url='login')
def topic(request, pk):
  topic = Topic.objects.get(id=pk)
  courses = Course.objects.select_related('topic').filter(topic=topic)
  list_count = NotificationList.objects.get(user=request.user).notification.all().count()

  context = {
    'courses':courses,
    'list_count': list_count, 
  }

  return render(request, 'topic.html', context)

