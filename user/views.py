from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.http import HttpResponse

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password

from .models import *
from course.models import Course
from quiz.models import Quiz, Result, Average_score
from follower.models import FollowList, FollowRequest

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

        try:
            Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            Profile.objects.create(user=user)

        return redirect('home')

    return render(request, 'register.html', context)

def checkUsername(request):
    username = request.POST.get('username').lower()

    if User.objects.filter(username=username).exists():
        return HttpResponse("This username already exists")
    else:
        return HttpResponse("This username is available")

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')

def forgotPass(request):
    pass

def get_follow_request_or_false(sender, reciever):
    try:
        return FollowRequest.objects.get(sender=sender, reciever=reciever, is_active=True)
    except FollowRequest.DoesNotExist:
        return False


@login_required(login_url='login')
def profilePath(request, pk):
    curr_user = User.objects.select_related('profile').get(id=pk)
    try:
        profile = Profile.objects.get(user=curr_user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=curr_user)
    courses = Course.objects.filter(host=pk)

    quiz_result = Average_score.objects.filter(user=curr_user)
    results = Result.objects.filter(user=curr_user)

    data = [{
        'id': 1,
    }]

    try:
        follow_list = FollowList.objects.get(user=curr_user)
    except FollowList.DoesNotExist:
        follow_list = FollowList.objects.create(user=curr_user)

    followers = follow_list.followers.all()

    is_self = True
    is_follower = False

    # FollowRequestStatus(Enum):
    # no_requet_sent = -1
    # them_sent_to_you = 0
    # you_sent_to_them = 1
    request_sent = -1
    follow_requests = None
    pending_follow_request_id = 0

    if request.user != curr_user:
        is_self = False
        if followers.filter(id=request.user.id):
            is_follower = True
        else:
            is_follower = False

            # them sent to you
            if get_follow_request_or_false(sender=curr_user, reciever=request.user) != False:
                request_sent = 0
                pending_follow_request_id = get_follow_request_or_false(sender=curr_user, reciever=request.user).id

            # you sent to them
            elif get_follow_request_or_false(sender=request.user, reciever=curr_user) != False:
                request_sent = 1

            # no request
            else:
                request_sent = -1

    follow_requests = FollowRequest.objects.filter(reciever=curr_user, is_active=True)

    count = Quiz.objects.annotate(child_count = models.Count('question_quiz')).filter(host=curr_user)

    context = {'curr_user': curr_user, 'profile': profile, 'courses': courses,
                'quizs': count, 'results': results, 'quiz_result': quiz_result,
                'followers': followers, 'is_self':is_self, 'is_follower': is_follower,
                'request_sent': request_sent, 'follow_requests': follow_requests,
                'pending_follow_request_id': pending_follow_request_id}

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

    return render(request, 'profile-update.html', context)

@login_required(login_url='login')
def userPath(request):
    users = User.objects.select_related('profile').exclude(id=request.user.id)

    if request.method == 'POST':
        username = request.POST.get('q').lower()

        if User.objects.filter(username__startswith=username).exists():
            users = User.objects.filter(username__startswith=username)

        elif username == '':
            users = User.objects.select_related('profile')
        else:
            messages.error(request, 'This user does not exist')
            return redirect('user-path')

    context = {'users': users}

    return render(request, 'user-path.html', context)

@login_required(login_url='login')
def profileResult(request, pk):
    context = {}
    return render(request, 'profile-result.html', context)
