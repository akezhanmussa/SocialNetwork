from django.urls import path
from . import views


urlpatterns = [
    path('', views.UserListView.as_view()),
    path('analytics/', views.UserAnalyticsView.as_view()),
    path('authentication/signup/', views.SignUpView.as_view()),
    path('authentication/login/', views.LoginView.as_view()),
]
