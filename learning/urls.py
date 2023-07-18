from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('user/', include('user.urls')),
    path('course/', include('course.urls')),
    # path('quiz/', include('quiz.urls')),
]
