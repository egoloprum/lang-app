from django.urls import path
from . import views

urlpatterns = [
    path('', views.contest, name='contest'),
    path('each/<str:pk>', views.eachContest, name='contest-each'),
    path('create', views.createContest, name='contest-create'),
    path('<str:pk>/edit', views.editContest, name='contest-edit'),

    path('<str:pk>/edit/quiz/create', views.createQuizFromContest, name='contest-quiz-create'),
    path('<str:pk>/edit/quiz/delete', views.deleteQuizFromContest, name='contest-quiz-delete'),
    path('<str:pk>/edit/quiz/<str:id>/edit', views.editQuizFromContest, name='contest-quiz-edit'),
]
