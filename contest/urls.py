from django.urls import path
from . import views

urlpatterns = [
    path('', views.contest, name='contest'),
    # path('each/<str:pk>', views.eachContest, name='contest-each'),
    path('create', views.createContest, name='contest-create'),
    path('<str:pk>/edit', views.editContest, name='contest-edit'),

    path('<str:pk>/edit/contest/create', views.createQuizFromContest, name='contest-quiz-create'),
    path('<str:pk>/edit/contest/<str:id>/edit', views.editQuizFromContest, name='contest-quiz-edit'),

    path('359', views.eachContest, name='contest-each'),
]
