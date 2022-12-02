from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from rest_framework import status
from django.conf import settings
from django.middleware import csrf


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
    'refresh': str(refresh),
    'access': str(refresh.access_token)
  }


class LoginView(APIView):
  def post(self, request):
    response = Response()

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
      tokens = get_tokens_for_user(user)

      response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_COOKIE'],
        value=tokens['access'],
        max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
      )

      csrf.get_token(request)

      response.data = { 'message': 'Login successfully' }
      response.status_code = 200
      return response
    else:
      return Response({ 'message': 'Invalid username or password.' }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
  def post(self, request):
    response = Response()

    response.delete_cookie('access_token')
    response.data = { 'message': 'You are logged out' }
    response.status_code = 200
    
    return response


class Me(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    return Response({
      'user': str(request.user),
    })
  
