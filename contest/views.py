from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

def contest(request):
    return render(request, 'contest.html')

def eachContest(request):
    return render(request, 'contest-each.html')

def createContest(request):
    pass

def editContest(request, pk):
    pass

def createQuizFromContest(request, pk):
    pass

def editQuizFromContest(request, pk, id):
    pass
