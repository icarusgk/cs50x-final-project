from django.urls import path
from api import views

urlpatterns = [
  path('auth/login', views.LoginView.as_view()),
  path('me', views.Me.as_view()),
]