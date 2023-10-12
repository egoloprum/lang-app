from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses', views.baseCourses, name='base-courses'),
    path('skills', views.baseSkills, name='base-skills'),
    path('grammar', views.baseGrammar, name='base-grammar'),
    path('business-english', views.baseBusEng, name='base-bus-eng'),
    path('general-english', views.baseGenEng, name='base-gen-eng'),
    path('english-level', views.baseEngLev, name='base-eng-lev'),

    path('calendar', views.calendar, name='calendar'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('daily_challenge', views.daily_challenge, name='daily_challenge'),
]
