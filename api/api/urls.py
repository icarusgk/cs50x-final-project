from django.urls import path, include
from api import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'workspaces', views.WorkSpaceView, 'workspace')
router.register(r'boards', views.BoardView, 'board')
router.register(r'cards', views.CardView, 'cards')

urlpatterns = [
  # Protected route
  path('me/', views.Me.as_view()),
  
  # Auth routes
  path('auth/register/', views.RegisterView.as_view()),
  path('auth/login/', views.CookieObtainTokenPairView.as_view()),
  # path('auth/token/refresh/', views.CookieRefreshTokenView.as_view()),
  path('auth/logout/', views.LogoutView.as_view()),

  # The router urls
  path('', include(router.urls)),
]