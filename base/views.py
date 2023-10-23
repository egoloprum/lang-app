from django.shortcuts import render, redirect
import math

# Create your views here.

def home(request):
    return render(request, 'index.html')

def subscribe(request):
    return render(request, 'subscribe.html')


def calendar(request):
    return render(request, 'calendar.html')




