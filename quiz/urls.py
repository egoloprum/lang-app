from django.urls import path
from . import views

urlpatterns = [
  path('', views.quiz, name='quiz'),
  path('create', views.quizCreate, name='quiz-create'),
  # path('login', views.loginUser, name='login'),
  # path('register', views.registerUser, name='register'),
  # path('logout', views.logoutUser, name='logout'),
  # path('forgot', views.forgotPass, name='forgot'),

  # path('profile/<str:pk>/', views.profilePath, name='profile'),
  # path('profile-update', views.profileUpdate, name='profile-update'),
  # path('delete', views.deleteUser, name='delete'), 
]
