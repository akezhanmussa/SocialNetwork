from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/users/', include('authentication.api.urls')),
    path('api/posts/', include('posts.api.urls')),
    path('admin/', admin.site.urls),
]
