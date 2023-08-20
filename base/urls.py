from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('daily_challenge', views.daily_challenge, name='daily_challenge'),
    path('store', views.store, name='store'),
    path('coins', views.store, name='coins'),
]
