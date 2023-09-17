from django.urls import path
from . import views

urlpatterns = [
  path('', views.course, name='course'),
  path('each/<str:pk>', views.eachCourse, name='course-each'),
  path('<str:pk>/content', views.eachChapter, name='content-each'),

  path('create', views.createCourse, name='course-create'),
  path('<str:pk>/edit', views.editCourse, name='course-edit'),

  path('<str:pk>/edit/chapter/create', views.createChapter, name='chapter-create'),
  path('<str:pk>/edit/chapter/<str:id>/edit', views.editChapter, name='chapter-edit'),

  path('<str:pk>/edit/quiz/create', views.createQuizFromCourse, name='course-quiz-create'),
  path('<str:pk>/edit/quiz/<str:id>/edit', views.editQuizFromCourse, name='course-quiz-edit'),

  path('chapter/<str:pk>/edit/quiz/create', views.createQuizFromChapter, name='chapter-quiz-create'),
  path('chapter/<str:pk>/edit/quiz/<str:id>/edit', views.editQuizFromChapter, name='chapter-quiz-edit'),

  path('topic/<str:pk>/', views.topic, name='topic'),

]
