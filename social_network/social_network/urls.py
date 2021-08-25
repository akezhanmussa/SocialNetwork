from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/users/', include('authentication.urls')),
    path('api/posts/', include('posts.urls')),
    path('admin/', admin.site.urls),
]
