from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import *
from quiz.models import Quiz

@login_required(login_url='login')
def createCourse(request):
  host = request.user
  course = Course.objects.create(host=host)
  course.name = f"New Course {course.id}"
  course.save()
  return redirect('course-edit', course.id)

@login_required(login_url='login')
def course(request):
  topics = Topic.objects.all()
  courses = Course.objects.select_related('host').order_by('-created_at')

  if request.method == 'POST':
    status = None if request.POST.get('course-status') == '' else request.POST.get('course-status')
    tag = None if request.POST.get('course-tags') == '' else request.POST.get('course-tags')
    topic = None if request.POST.get('course-topics') == '' else request.POST.get('course-topics')
    date = None if request.POST.get('course-date') == '' else request.POST.get('course-date')
    search = None if request.POST.get('course-search') == '' else request.POST.get('course-search')

    return redirect('course')

  if request.user.is_staff:
    context = {'topics': topics, 'courses': courses}
  else:
    courses = courses.filter(publication=True)
    context = {'topics': topics, 'courses': courses}

  return render(request, 'course.html', context)

@login_required(login_url='login')
def editCourse(request, pk):
  course = Course.objects.select_related('host').get(id=pk)
  quizs = Quiz.objects.select_related('course').filter(course=course).annotate(questions_count=models.Count('question_quiz'))
  contents = Content.objects.select_related('course').filter(course=course)
  contents = contents.annotate(quizs_count=models.Count('quiz_content'), files_count=models.Count('file_content'))
  topics = Topic.objects.all()
  tags = Tag.objects.all()

  if request.method == 'POST':
    name = request.POST.get('course-name')
    topic = request.POST.get('course-topic')
    tag = request.POST.get('course-tag')
    body = request.POST.get('course-body')
    start = request.POST.get('course-start')
    end = request.POST.get('course-end')
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

  context = {
    'course': course,
    'quizs': quizs,
    'contents': contents,
    'topics': topics,
    'tags': tags,
    'cour_files': course_files,
    'cont_files': content_files,
  }

  return render(request, 'course-edit.html', context)

@login_required(login_url='login')
def eachCourse(request, pk):
  course = Course.objects.get(id=pk)
  contents = Content.objects.filter(course=course)
  files = File.objects.filter(course=course)
  context = {
    'course': course,
    'contents': contents,
    'files': files,
  }
  return render(request, 'course-each.html', context)

@login_required(login_url='login')
def eachChapter(request, pk):
   content = Content.objects.get(id=pk)
   course = Course.objects.select_related('host').get(id=content.course.id)
   contents = Content.objects.filter(course=course)

   context = {'content': content, 'course': course, 'contents': contents}
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
  print(id, pk)
  content = Content.objects.get(id=id)
  course = Course.objects.get(id=pk)
  quizs = Quiz.objects.filter(content=content).annotate(questions_count=models.Count('question_quiz'))

  context = {
    'content': content,
    'course': course,
    'quizs': quizs,
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

  context = {'courses':courses }

  return render(request, 'topic.html', context)

