from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
    'refresh': str(refresh),
    'access': str(refresh.access_token)
  }


# The http-only refresh token serializer that includes the
# refresh token when trying to refresh
class CookieRefreshTokenSerializer(TokenRefreshSerializer):
  refresh = None
  def validate(self, attrs):
    # Get the refresh token from the request session
    # and set the 'refresh' key in attrs to it
    attrs['refresh'] = self.context['request'].session.get('refresh')
    if attrs['refresh']:
      return super().validate(attrs)
    else:
      raise InvalidToken('No valid token found in cookie \'refresh_token\'')


# The user's login
class CookieObtainTokenPairView(TokenObtainPairView):
  def finalize_response(self, request, response, *args, **kwargs):
    # Check for the 'refresh' key from the response
    if response.data.get('refresh'):
      # 1 day
      access_max_age = 3600 * 24
      response.set_cookie('access_token', response.data['access'], max_age=access_max_age, httponly=True, samesite='None', secure=True)
      request.session['refresh'] = response.data['refresh']

      # Remove the tokens from the JSON response
      del response.data['access']
      del response.data['refresh']
    return super().finalize_response(request, response, *args, **kwargs)


# Refreshes the user's access_token
class CookieRefreshTokenView(TokenRefreshView):
  def finalize_response(self, request, response, *args, **kwargs):
    if response.data.get('access'):
      # 1 day
      access_max_age = 3600 * 24
      response.set_cookie('access_token', response.data['access'], max_age=access_max_age, httponly=True, samesite='None', secure=True)
      # Remove the tokens from the JSON response
      del response.data['access']
    return super().finalize_response(request, response, *args, **kwargs)
  serializer_class = CookieRefreshTokenSerializer



class LogoutView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request):
    response = Response()

    # Delete the token and the session
    response.delete_cookie('access_token')

    response.delete_cookie('sessionid')
    request.session = {}

    response.data = { 'message': 'You are logged out' }
    response.status_code = 200
    return response


# Protected API view
class Me(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    return Response({
      'user': str(request.user),
      'session': request.session
    })

