from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    return render(request, 'index.html')

def subscribe(request):
    return render(request, 'subscribe.html')

def daily_challenge(request):
    return render(request, 'daily-challenge.html')

def store(request):
    return render(request, 'store.html')

def contest(request):
    return render(request, 'contest.html')

def contestEach(request):
    return render(request, 'contest-each.html')

def calendar(request):
    return render(request, 'calendar.html')

def baseCourses(request):
    return render(request, 'home.html')

def baseSkills(request):
    return render(request, 'home.html')

def baseGrammar(request):
    return render(request, 'home.html')

def baseBusEng(request):
    return render(request, 'home.html')

def baseGenEng(request):
    return render(request, 'home.html')

def baseEngLev(request):
    return render(request, 'home.html')



