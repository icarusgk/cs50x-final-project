from django.urls import path, include
from api import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'workspace', views.WorkSpace, 'workspace')

urlpatterns = [
  # Protected route
  path('me/', views.Me.as_view()),

  # Auth routes
  path('auth/register/', views.RegisterView.as_view()),
  path('auth/login/', views.CookieObtainTokenPairView.as_view()),
  path('auth/token/refresh/', views.CookieRefreshTokenView.as_view()),
  path('auth/logout/', views.LogoutView.as_view()),
  path('', include(router.urls)),
]