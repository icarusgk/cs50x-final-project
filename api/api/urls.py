from django.urls import path
from api import views

urlpatterns = [
  # Protected route
  path('me', views.Me.as_view()),

  # Auth routes
  path('auth/login', views.CookieObtainTokenPairView.as_view()),
  path('auth/token/refresh', views.CookieRefreshTokenView.as_view()),
  path('auth/logout', views.LogoutView.as_view()),
]