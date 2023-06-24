from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users.views import home

urlpatterns = [
    path('haker/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/ariza/', include('ariza.urls')),
    path('', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
