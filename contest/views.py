from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from quiz.models import Quiz

# Create your views here.

def contest(request):
    contests = Contest.objects.select_related('host')
    context = {
        'contests': contests,
    }
    return render(request, 'contest.html', context)

def eachContest(request, pk):
    contest = Contest.objects.get(id=pk)
    quizs = Quiz.objects.filter(contest=contest)
    context = {
        'contest': contest,
        'quizs': quizs,
    }
    return render(request, 'contest-each.html', context)

def createContest(request):
    contest = Contest.objects.create(host=request.user)
    return redirect('contest-edit', contest.id)

def editContest(request, pk):
    contest = Contest.objects.get(id=pk)
    quizs = Quiz.objects.filter(contest=contest)
    context = {
        'contest': contest,
        'quizs': quizs,
    }

    if request.method == 'POST':
        name = None if request.POST.get('contest-name') == '' else request.POST.get('contest-name')
        body = None if request.POST.get('contest-body') == '' else request.POST.get('contest-body')
        pts = None if request.POST.get('contest-pts') == '' else request.POST.get('contest-pts')
        exp = None if request.POST.get('contest-exp') == '' else request.POST.get('contest-exp')
        start_date = None if request.POST.get('contest-start') == '' else request.POST.get('contest-start')
        end_date = None if request.POST.get('contest-end') == '' else request.POST.get('contest-end')
        public = True if request.POST.get('contest-public') == 'on' else False

        contest.name = name
        contest.body = body
        contest.pts = pts
        contest.exp = exp
        contest.start_date = start_date
        contest.end_date = end_date
        contest.publication = public
        contest.save()

        return redirect('contest')

    return render(request, 'contest-edit.html', context)

def createQuizFromContest(request, pk):
    contest = Contest.objects.get(id=pk)
    try:
        quiz = Quiz.objects.create(host=request.user, contest=contest)
        return HttpResponse(quiz.id)
    except Exception:
        return HttpResponse("Quiz create error")

def editQuizFromContest(request, pk, id):
    pass

def deleteQuizFromContest(request, pk):
    quiz = Quiz.objects.get(id=pk)
    try:
        quiz.delete()
        return HttpResponse('Quiz is successfully deleted')
    except Exception:
        return HttpResponse('Quiz delete error')
