from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses', views.baseCourses, name='base-courses'),
    path('skills', views.baseSkills, name='base-skills'),
    path('grammar', views.baseGrammar, name='base-grammar'),
    path('vocabulary', views.baseVocab, name='base-vocab'),
    path('business-english', views.baseBusEng, name='base-bus-eng'),
    path('general-english', views.baseGenEng, name='base-gen-eng'),
    path('english-level', views.baseEngLev, name='base-eng-lev'),


    path('subscribe', views.subscribe, name='subscribe'),
    path('daily_challenge', views.daily_challenge, name='daily_challenge'),
    path('store', views.store, name='store'),
    path('coins', views.store, name='coins'),
    path('contest', views.contest, name='contest'),
    path('contest/359', views.contestEach, name='contest-each'),
]
