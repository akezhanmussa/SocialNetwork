from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostView.as_view()),
    path('operation/', views.PostOperationView.as_view()),
    path('analytics/', views.PostAnalyticsView.as_view()),
]
