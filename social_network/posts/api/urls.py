from django.urls import path
from posts.api import views

urlpatterns = [
    path('', views.PostView.as_view()),
    path('create/', views.PostCreateView.as_view()),
    path('operation/', views.PostOperationView.as_view()),
    path('analytics/', views.PostAnalyticsView.as_view()),
]
