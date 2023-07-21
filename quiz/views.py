from django.shortcuts import render, redirect

# Create your views here.

def quiz(request):
    context = {}
    return render(request, 'quiz.html', context)

def quizCreate(request):
    context = {}
    return render(request, 'quiz-create.html', context)
