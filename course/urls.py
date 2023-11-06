from django.urls import path
from . import views

urlpatterns = [
  path('', views.course, name='course'),
  path('search-course', views.searchCourse, name='course-search'),
  path('each/<str:pk>', views.eachCourse, name='course-each'),
  path('each/<str:pk>/result', views.resultCourse, name='course-result'),
  path('<str:pk>/content', views.eachChapter, name='content-each'),

  path('create', views.createCourse, name='course-create'),
  path('<str:pk>/edit', views.editCourse, name='course-edit'),
  path('<str:pk>/delete', views.deleteCourse, name='course-delete'),

  path('<str:pk>/edit/chapter/create', views.createChapter, name='chapter-create'),
  path('edit/chapter/<str:pk>/delete', views.deleteChapter, name='chapter-delete'),
  path('<str:pk>/edit/chapter/<str:id>/edit', views.editChapter, name='chapter-edit'),

  path('<str:pk>/edit/quiz/create', views.createQuizFromCourse, name='course-quiz-create'),
  path('edit/quiz/<str:pk>/delete', views.deleteQuizFromCourse, name='course-quiz-delete'),

  path('chapter/<str:pk>/edit/quiz/create', views.createQuizFromChapter, name='chapter-quiz-create'),
  path('chapter/edit/quiz/<str:pk>/delete', views.deleteQuizFromChapter, name='chapter-quiz-delete'),

  path('topic/<str:pk>/', views.topic, name='topic'),

]
