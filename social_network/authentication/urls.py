from django.urls import path
from . import views


urlpatterns = [
    path('users/signup', views.SignUpView.as_view()),
    path('users/login', views.LoginView.as_view()),
]
