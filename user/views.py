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
from django.db.models import Q
from course.models import Course
from quiz.models import Quiz, Result
from follower.models import FollowList, FollowRequest, NotificationList

from faker import Faker


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
            try:
                Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=user)
                profile.badge.add(Badge.objects.get(name='Welcome to English Study'))
                profile.save()

            try:
                FollowList.objects.get(user=user)
            except FollowList.DoesNotExist:
                FollowList.objects.create(user=user)

            try:
                NotificationList.objects.get(user=user)
            except NotificationList.DoesNotExist:
                NotificationList.objects.create(user=user)

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
            messages.error(request, 'Your password does not match standart')
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
            profile = Profile.objects.create(user=user)
            profile.badge.add(Badge.objects.get(name='Welcome to English Study'))
            profile.save()

        try:
            NotificationList.objects.get(user=user)
        except NotificationList.DoesNotExist:
            NotificationList.objects.create(user=user)

        return redirect('home')

    return render(request, 'register.html', context)

def checkUsername(request):
    username = request.POST.get('username').lower()

    if User.objects.filter(username=username).exists():
        return HttpResponse("<p>This username already exists</p>")
    else:
        return HttpResponse("<p>This username is okay</p>")
    
def checkPassword(request):
    password = request.POST.get('password')

    try:
        validate_password(password)
    except Exception:
        return HttpResponse("<p>bad password</p>")
    
    return HttpResponse("<p>okay password</p>")

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
def dashboardPath(request, pk):
    curr_user = User.objects.select_related('user').get(id=pk)
    list_count = NotificationList.objects.get(user=request.user).notification.all().count()

    context = {}
    context['curr_user'] = curr_user
    context['list_count'] = list_count

    quizs = Quiz.objects.select_related().filter(course=None, content=None)
    courses = Course.objects.select_related()

    if curr_user.is_staff:
        all_quizs = quizs
        all_courses = courses
        quizs = quizs.annotate(child_count = models.Count('question_quiz')).filter(host=curr_user)
        courses = courses.filter(host=pk)

        context['quizs'] = quizs
        context['courses'] = courses
        context['all_quizs'] = all_quizs
        context['all_courses'] = all_courses
    
    else:
        results = Result.objects.filter(user=curr_user, has_course=None, has_content=None).select_related('quiz')
        context['results'] = results

        quiz_count = quizs.filter(publication=True).count()
        course_count = courses.filter(publication=True).count()

        context['quiz_count'] = quiz_count
        context['course_count'] = course_count

        quizs_easy = 0
        quizs_medium = 0
        quizs_hard = 0

        for quiz in quizs:
            if quiz.difficulty == 'Easy':
                quizs_easy += 1
            if quiz.difficulty == 'Medium':
                quizs_medium += 1
            if quiz.difficulty == 'Hard':
                quizs_hard += 1

        comp_easy = 0
        comp_medium = 0
        comp_hard = 0

        completions = Completion.objects.select_related('quiz', 'user').filter(user=curr_user, course=None, content=None)
        for comp in completions:
            if comp.quiz.difficulty == 'Easy':
                comp_easy += 1
            if comp.quiz.difficulty == 'Medium':
                comp_medium += 1
            if comp.quiz.difficulty == 'Hard':
                comp_hard += 1

        context['comp_easy'] = comp_easy
        context['comp_medium'] = comp_medium
        context['comp_hard'] = comp_hard

        context['quizs_easy'] = quizs_easy
        context['quizs_medium'] = quizs_medium
        context['quizs_hard'] = quizs_hard
        context['quizs'] = quizs

        completions = Completion.objects.select_related()

        try:
            complete_quiz = completions.filter(user=curr_user, completed=True, course=None, content=None)
        except Completion.DoesNotExist:
            complete_quiz = None

        try:
            complete_course = completions.filter(user=curr_user, completed=True, quiz=None, content=None)
        except Completion.DoesNotExist:
            complete_course = None
        
        context['complete_quiz'] = complete_quiz
        context['complete_course'] = complete_course

    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def profilePath(request, pk):
    curr_user = User.objects.select_related('profile').get(id=pk)
    list_count = NotificationList.objects.get(user=request.user).notification.all().count()

    context = {}
    context['list_count'] = list_count

    try:
        profile = Profile.objects.get(user=curr_user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=curr_user)
        profile.badge.add(Badge.objects.get(name='Welcome to English Study'))
        profile.save()
        
    badges = profile.badge.all()

    context['curr_user'] = curr_user
    context['profile'] = profile
    context['badges'] = badges

    try:
        follow_list = FollowList.objects.get(user=curr_user)
    except FollowList.DoesNotExist:
        follow_list = FollowList.objects.create(user=curr_user)

    followers = follow_list.followers.all()
    if followers.count() > 0:
        profile.badge.add(Badge.objects.get(name="Let's get friends"))

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

    courses = Course.objects.select_related('host').filter(host=curr_user)
    context['courses'] = courses

    context['follow_requests'] = follow_requests
    context['followers'] = followers
    context['is_self'] = is_self
    context['is_follower'] = is_follower
    context['request_sent'] = request_sent
    context['pending_follow_request_id'] = pending_follow_request_id

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
    user = User.objects.select_related('profile').get(id=request.user.id)
    list_count = NotificationList.objects.get(user=request.user).notification.all().count()

    context = {'user': user, 'list_count': list_count,}

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
                user_profile.badge.add(Badge.objects.get(name='New Look'))
            user_profile.save()

            return redirect('profile', user.id)

        if request.path == '/user/profile-update/account':
            user_name = request.POST.get('username')
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

    return render(request, 'profile-update.html', context)

@login_required(login_url='login')
def profileDelete(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def userPath(request):
    list_count = NotificationList.objects.get(user=request.user).notification.all().count()
    profiles = Profile.objects.select_related('user').exclude(id=request.user.id).order_by('-points')
    users = User.objects.select_related('profile').exclude(id=request.user.id)

    users = list(zip(users, profiles))

    context = {'list_count': list_count, 'users': users}
    return render(request, 'user-path.html', context)

def searchUserpath(request):
    search_users = request.POST.get('search-users')
    search_type = request.POST.get('search-type')
    search_level = request.POST.get('search-level')
    search_country = request.POST.get('search-country')
    search_gender = request.POST.get('search-gender')
    search_birthday = request.POST.get('search-birthday')

    profiles = Profile.objects.select_related('user').exclude(id=request.user.id).order_by('points')
    base_users = User.objects.select_related('profile').exclude(id=request.user.id)

    search_value = 0

    # searching by level
    if search_level == 'Ascending':
        profiles = profiles.order_by('level')
        users = list(zip(base_users, profiles))
        search_value = 1

    elif search_level == 'Descending':
        profiles = profiles.order_by('-level')
        users = list(zip(base_users, profiles))
        search_value = 1

    # searching by country
    if search_country == 'Ascending':
        profiles = profiles.order_by('country')
        users = list(zip(base_users, profiles))
        search_value = 1

    elif search_country == 'Descending':
        profiles = profiles.order_by('-country')
        users = list(zip(base_users, profiles))
        search_value = 1

    # searching by gender
    if search_gender == 'Male':
        profiles = profiles.filter(Q(gender='M'))
        users = list(zip(base_users, profiles))
        search_value = 1

    elif search_gender == 'Female':
        profiles = profiles.filter(Q(gender='F'))
        users = list(zip(base_users, profiles))
        search_value = 1

    # searching by birthday
    if search_birthday == 'Ascending':
        profiles = profiles.order_by('birthday')
        users = list(zip(base_users, profiles))
        search_value = 1

    elif search_birthday == 'Descending':
        profiles = profiles.order_by('-birthday')
        users = list(zip(base_users, profiles))      
        search_value = 1

    # searching by role
    if search_type == 'Staff':
        base_users = base_users.filter(Q(is_staff=True))
        users = list(zip(base_users, profiles))    
        search_value = 1

    elif search_type == 'User':
        base_users = base_users.filter(Q(is_staff=False))
        users = list(zip(base_users, profiles))
        search_value = 1

    # searching by name
    if search_users:
        base_users = base_users.filter(Q(username__icontains=search_users))
        users = list(zip(base_users, profiles))
        search_value = 1

    context = {}

    if search_value == 0:
        context['users'] = list(zip(base_users, profiles))

    elif search_value == 1:
        context['users'] = users

    return render(request, 'user-path-partial.html', context)

def badges(request):
    badges = Badge.objects.select_related()
    list_count = NotificationList.objects.get(user=request.user).notification.all().count()

    context = {
        'badges': badges,
        'list_count': list_count,
    }
    return render(request, 'badges.html', context)
