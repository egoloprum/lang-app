from django.urls import path
from . import views

urlpatterns = [
  path('', views.course, name='course'),
  path('each/<str:pk>', views.courseEach, name='course-each'),
  path('each/<str:pk>/content', views.courseEachContent, name='course-each-content'),

  path('each/<str:pk>/edit', views.courseEachEdit, name='course-each-edit'),
  path('create', views.createCourse, name='create-course'),
  path('topic/<str:pk>/', views.topic, name='topic'),

  # path('login', views.loginUser, name='login'),
  # path('register', views.registerUser, name='register'),
  # path('logout', views.logoutUser, name='logout'),
  # path('forgot', views.forgotPass, name='forgot'),

  # path('profile/<str:pk>/', views.profilePath, name='profile'),
  # path('profile-update', views.profileUpdate, name='profile-update'),
  # path('delete', views.deleteUser, name='delete'), 
]
