from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import *


@login_required(login_url='login')
def followerList(request, pk):
    curr_user = User.objects.get(id=pk)
    context = {}

    try:
        follow_list = FollowList.objects.get(user=curr_user)
        follow_list = follow_list.followers.all()
        context['follow_list'] = follow_list

    except FollowList.DoesNotExist:
        context['follow_list'] = None
        return HttpResponse(f"Could not find a friends list for {curr_user.username}")
    
    try:
        follow_requests = FollowRequest.objects.filter(reciever=curr_user, is_active=True)
        context['follow_requests'] = follow_requests
    except FollowRequest.DoesNotExist:
        HttpResponse('Something is wrong')
        
    try:
        follow_requests_sent = FollowRequest.objects.filter(sender=curr_user, is_active=True)
        context['follow_requests_sent'] = follow_requests_sent
    except FollowRequest.DoesNotExist:
        HttpResponse('Something is wrong')
        
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

    return redirect(request.META.get('HTTP_REFERER'))
    # return redirect('/user/profile/%d/'%reciever.id)

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

    return redirect(request.META.get('HTTP_REFERER'))
    # return redirect('/follower/%d/'%request.user.id)

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

    return redirect(request.META.get('HTTP_REFERER'))
    # return redirect('/follower/%d/'%request.user.id)

@login_required(login_url='login')
def decline_follow(request, pk):
    removee = User.objects.get(id=pk)

    follow_list = FollowList.objects.get(user=request.user)
    follow_list.unfollow(removee)

    return redirect(request.META.get('HTTP_REFERER'))
    # return redirect('/user/profile/%d/'%removee.id)

@login_required(login_url='login')
def chatRoom(request):
    chatrooms = ChatRoom.objects.select_related('host')
    context = {
        'chatrooms': chatrooms,
    }

    return render(request, 'chatroom.html', context)

def createChatroom(request, pk):
    host = request.user
    chatter = User.objects.get(id=pk)
    try:
        chatroom = ChatRoom.objects.get(host=host, name=f"{host.username} + {chatter.username}")
        return redirect('chatroom')
    
    except ChatRoom.DoesNotExist:
        chatroom = ChatRoom.objects.create(host=host, name=f"{host.username} + {chatter.username}")
        chatroom.add(chatter)
        return redirect('chatroom')

@login_required(login_url='login')
def eachChat(request, pk):
    chatroom = ChatRoom.objects.get(id=pk)
    chatroom.user.add(request.user)

    out_users = User.objects.filter(chatroom_user=None)

    chatroom_users = chatroom.user.all()

    messages = Message.objects.select_related('user').filter(room=chatroom)

    context = {
        'chatroom': chatroom,
        'messages': messages,
        'out_users': out_users,
        'chatroom_users': chatroom_users,
    }

    return render(request, 'chat-each.html', context)
