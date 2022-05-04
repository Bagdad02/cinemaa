from django.urls import path, include

from django.contrib import admin

apipatterns = [
    path('', include('urls')),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(apipatterns, namespace='api')),
]