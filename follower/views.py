from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import *


# Create your views here.

@login_required(login_url='login')
def followerList(request, pk):
    curr_user = User.objects.get(user=pk)
    context = {}

    try:
        follow_list = FollowList.objects.get(user=pk)
        follow_list = follow_list.followers.all()
        context['follow_list'] = follow_list

    except FollowList.DoesNotExist:
        context['follow_list'] = None
        return HttpResponse(f"Could not find a friends list for {curr_user.username}")
    
    if curr_user == request.user:
        follow_requests = FollowRequest.objects.filter(reciever=curr_user, is_active=True)
        context['follow_requests'] = follow_requests
        
    context['curr_user'] = curr_user

    return render(request, 'followers.html', context)

@login_required(login_url='login')
def send_follow_request(request, pk):
    payload = ""

    reciever = User.objects.get(id=pk)

    follow_requests = FollowRequest.objects.filter(sender=request.user, reciever=reciever, is_active=True)
    if follow_requests:
        payload = 'You already sent a follow request.'

    else:
        follow_request = FollowRequest.objects.create(sender=request.user, reciever=reciever)
        payload = "Follow request sent."

    return redirect('/user/profile/%d/'%reciever.id)

# from request user side
@login_required(login_url='login')
def cancel_follow_request(request, pk):
    payload = ""
    reciever = User.objects.get(id=pk)

    follow_requests = FollowRequest.objects.filter(sender=request.user, reciever=reciever, is_active=True)
    if follow_requests:
        follow_requests.delete()
        payload = "Follow request has been cancelled"
    else:
        payload = "There is no follow request"

    return redirect('/user/profile/%d/'%reciever.id)

# from reciever side
@login_required(login_url='login')
def cancel_request(request, pk):
    payload = ""
    try:
        follow_request = FollowRequest.objects.get(id=pk)
    except FollowRequest.DoesNotExist:
        return HttpResponse('Something is wrong')
    if follow_request:
        follow_request.delete()
        payload = "Follow request has been cancelled"
    else:
        payload = "There is no follow request"

    return redirect('/follower/%d/'%request.user.id)

@login_required(login_url='login')
def accept_follow_request(request, pk):
    payload = ""
    try:
        follow_request = FollowRequest.objects.get(id=pk)
    except FollowRequest.DoesNotExist:
        return HttpResponse('Something is wrong')

    if follow_request:
        follow_request.accept()
        follow_request.delete()
        payload = "Follow request has been accepted"
    else:
        payload = "There is no follow request"

    return redirect('/follower/%d/'%request.user.id)

@login_required(login_url='login')
def decline_follow(request, pk):
    removee = User.objects.get(id=pk)

    follow_list = FollowList.objects.get(user=request.user)
    follow_list.unfollow(removee)

    return redirect('/profile/%d/'%removee.id)
