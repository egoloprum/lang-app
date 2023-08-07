from django.urls import path
from . import views

urlpatterns = [
  path('<str:pk>/', views.followerList, name='followers'),
  path('<str:pk>/send_follow_request', views.send_follow_request, name='send-follow-request'),
  path('<str:pk>/cancel_follow_request', views.cancel_follow_request, name='cancel-follow-request'),
]
