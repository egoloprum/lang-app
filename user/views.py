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

        if user:
            login(request, user)
            user.profile.active = True
            user.profile.save()
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
        return HttpResponse("<p>This username already exists</p>")
    else:
        return HttpResponse("")

@login_required(login_url='login')
def logoutUser(request):
    user = User.objects.get(id=request.user.id)
    user.profile.active = False
    user.save()
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
    results = Result.objects.filter(user=curr_user).select_related('quiz')

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
    user = User.objects.get(id=request.user.id)
    context = {'user': user}

    if request.method == "POST":
        if request.path == '/user/profile-update':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = None if request.POST.get('gender') == '' else request.POST.get('gender') 
            country = None if request.POST.get('country') == '' else request.POST.get('country')
            avatar = None if request.FILES.get('picture') == '' else request.FILES.get('picture')

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            user_profile = Profile.objects.get(user=user)
            user_profile.gender = gender
            user_profile.country = country
            if avatar:
                user_profile.avatar = avatar
            user_profile.save()

            return redirect('profile', user.id)

        if request.path == '/user/profile-update/account':
            user_name = request.POST.get('user_name')
            email = request.POST.get('email')
            cur_password = request.POST.get('current-password')
            new_password = request.POST.get('password')

            if check_password(cur_password, user.password):
                if user_name:
                    user.username = user_name
                    try:
                        user.save()
                    except:
                        messages.error(request, 'This username is already taken')
                        return redirect('profile-update-account')
                if email:
                    user.email = email
                    try:
                        user.save()
                    except:
                        messages.error(request, 'This email is already used')
                        return redirect('profile-update-account')
                if new_password:
                    try:
                        validate_password(new_password)
                    except ValidationError:
                        messages.error(request, 'Your password is not strong enough')
                        return redirect('profile-update-account')
                    user.password = make_password(new_password)
                    user.save()

            else:
                messages.error(request, 'Wrong password input')
                return redirect('profile-update-account')
            
            login(request, user)
            messages.success(request, 'Profile has been updated')
            return redirect('profile-update-account')

        else:
            messages.error(request, "Please enter correct password")
            return redirect('profile-update-account')

    return render(request, 'profile-update.html', context)

@login_required(login_url='login')
def userPath(request):
    users = User.objects.select_related('profile').exclude(id=request.user.id)

    if request.method == 'POST':
        username = request.POST.get('q').lower()

        if users.filter(username__startswith=username).exists():
            users = users.filter(username__startswith=username)
            return redirect('user-path')

        elif username == '':
            users = users
            return redirect('user-path')
        else:
            messages.error(request, 'This user does not exist')
            return redirect('user-path')

    context = {'users': users}

    return render(request, 'user-path.html', context)

@login_required(login_url='login')
def profileResult(request, pk):
    context = {}
    return render(request, 'profile-result.html', context)
