from django.urls import path
from . import views

urlpatterns = [
  path('login', views.loginUser, name='login'),
  path('register/', views.registerUser, name='register'),
  path('register/check_username', views.checkUsername, name='check-username'),
  path('register/check_password', views.checkPassword, name='check-password'),

  path('logout', views.logoutUser, name='logout'),
  path('forgot', views.forgotPass, name='forgot'),

  path('dashboard/<str:pk>', views.dashboardPath, name='dashboard'),
  path('profile/<str:pk>/', views.profilePath, name='profile'),

  path('profile-update', views.profileUpdate, name='profile-update'),
  path('profile-update/points', views.profileUpdate, name='profile-update-points'),
  path('profile-update/account', views.profileUpdate, name='profile-update-account'),
  path('profile-update/notifications', views.profileUpdate, name='profile-update-notif'),
  path('profile-delete/<str:pk>', views.profileDelete, name='profile-delete'),

  path('delete', views.deleteUser, name='delete'), 

  path('user-path', views.userPath, name='user-path'),
  path('badges', views.badges, name='badges'),
]

