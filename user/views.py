from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password

from .models import *
from course.models import Course
from quiz.models import Quiz, Result, Average_score

def loginUser(request):
    context = {}

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password does not match")

    return render(request, 'login.html', context)

def registerUser(request):
    context = {}

    if request.method == "POST":
        password = request.POST.get("password")
        username = request.POST.get("username").lower()
        email = request.POST.get("email")

        try:
            validate_password(password)
        except ValidationError:
            messages.error(request, 'Your password sucks')
            return redirect('register')
        
        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        
        user.save()
        login(request, user)
        Profile.objects.create(user=user)
        return redirect('home')

    return render(request, 'register.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')

def forgotPass(request):
    pass

@login_required(login_url='login')
def profilePath(request, pk):
    user = User.objects.get(id=pk)
    profile = Profile.objects.get(user=pk)
    courses = Course.objects.filter(host=pk)
    quizs = Quiz.objects.filter(host=user)

    quiz_result = Quiz.objects.all()
    results = Result.objects.filter(user=user)

    average_score = Average_score.objects.filter(user=user)

    context = {'user': user, 'profile': profile, 'courses': courses, 'average_score': average_score,
                'quizs': quizs, 'results': results, 'quiz_result': quiz_result}

    return render(request, 'profile.html', context)


@login_required(login_url='login')
def deleteUser(request):
    user = request.user
    context = {'user':user}

    if request.method == "POST":
        pass1 = request.POST.get("password")
        if check_password(pass1, user.password):
            user.delete()
            logout(request)
            return redirect('home')
        else:
            messages.error(request, "Your password is wrong")
            return redirect('delete')

    return render(request, 'delete.html', context)


@login_required(login_url='login')
def profileUpdate(request):
    user = request.user
    context = {'user': user}

    if request.method == "POST":
        user_name = request.POST.get('user_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        cur_password = request.POST.get('current-password')
        password = request.POST.get('password')

        if check_password(cur_password, user.password):
            if email:
                user.email = email
                try:
                    user.save()
                except:
                    messages.error(request, 'This email is already used')
                    return redirect('profile-update')
            if password:
                try:
                    validate_password(password)
                except ValidationError:
                    messages.error(request, 'Your password sucks')
                    return redirect('profile-update')
                user.password = make_password(password)
                user.save()
            if first_name:
                user.first_name = first_name
                user.save()
            if last_name:
                user.last_name = last_name
                user.save()
            
            login(request, user)
            # profile.get_or_create(first_name=first_name, last_name=last_name)
            return redirect('profile/%d/'%request.user.id)

        else:
            messages.error(request, "Please enter correct password")
            return redirect('profile-update')

    return render(request, 'profileUpdate.html', context)
