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
