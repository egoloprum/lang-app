from django.urls import path
from . import views

urlpatterns = [
  path('', views.quiz, name='quiz'),
  path('create', views.quizCreate, name='quiz-create'),
  path('check_quiz_name', views.checkQuizName, name='check-quiz-name'),

  path('<str:pk>', views.quizEach, name='quiz-each'),
  path('each/<str:pk>/result', views.quizResult, name='quiz-result'),
  path('each/<str:pk>/edit', views.quizEdit, name='quiz-edit'),
  path('each/<str:pk>/delete', views.quizDelete, name='quiz-delete'),
  path('<str:pk>/add-question', views.add_question, name='add-question'),
  path('<str:pk>/add-answer', views.add_answer, name='add-answer'),
  path('<str:pk>/delete-question', views.delete_question, name='delete-question'),
  path('<str:pk>/delete-answer', views.delete_answer, name='delete-answer'),
  # path('each/<str:pk>/result', views.quizResult, name='quiz-result'),
]
