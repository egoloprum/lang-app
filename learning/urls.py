from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('user/', include('user.urls')),
    path('course/', include('course.urls')),
    path('quiz/', include('quiz.urls')),
    path('follower/', include('follower.urls')),

    path("__debug__/", include("debug_toolbar.urls")),
]

handler404 = "base.views.custom_page_not_found_view"
handler500 = "base.views.custom_error_view"
handler403 = "base.views.custom_permission_denied_view"
handler400 = "base.views.custom_bad_request_view"

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
