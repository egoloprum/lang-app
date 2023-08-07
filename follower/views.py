from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import *


# Create your views here.

@login_required(login_url='login')
def followerList(request, pk):
    curr_user = User.objects.get(user=pk)

    try:
        followers = FollowList.objects.get(user=pk)
    except FollowList.DoesNotExist:
        followers = []
        return HttpResponse(f"Could not find a friends list for {curr_user.username}")
    
    follow_requests = []
    
    if curr_user == request.user:
        follow_requests = FollowRequest.objects.filter(reciever=curr_user, is_active=True)

    context = {'followers': followers, 'follow_requests': follow_requests}

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
