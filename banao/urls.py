from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('user.urls')),
    path('api/', include('blogs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)