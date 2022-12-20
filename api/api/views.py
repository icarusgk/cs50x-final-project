from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from api.models import *
from api.serializers import *
from rest_framework import permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.conf import settings


# The user's login, it inherits from TokenObtainPairView
class CookieObtainTokenPairView(TokenObtainPairView):
  def finalize_response(self, request, response, *args, **kwargs):
    """
    Customize the response of the JWT tokens

    So that instead of returning the tokens in the response
    the access token is set as a cookie and the refresh token
    is stored in the user session.
    """
    # Check for the 'refresh' key from the response
    if response.data.get('refresh'):
      # Set the cookie
      response.set_cookie('access_token', response.data['access'], max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'], httponly=True, samesite='None', secure=True)

      # Set the session token
      request.session['refresh'] = response.data['refresh']

      # Add a message to the response
      response.data['message'] = 'Successfully logged in!'

      # Remove the tokens from the JSON response
      del response.data['access']
      del response.data['refresh']
      # Call the super method
    return super().finalize_response(request, response, *args, **kwargs)



class WorkSpaceView(ModelViewSet):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = WorkSpaceSerializer

  def get_queryset(self):
    """
    Return the current user's workspaces
    """
    return self.request.user.workspaces
  
  def retrieve(self, request, pk=None):
    """
    Customizes the response so that it includes the
    name of the workspace as well as the boards
    """
    ws = self.get_object()
    return Response({
      "name": ws.name,
      "boards": BoardSerializer(ws.boards.all(), many=True).data
    })

  # Include the user on workspace creation
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)



class BoardView(ModelViewSet):
  queryset = Board.objects.all()
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = BoardSerializer

  def get_queryset(self):
    """
    Return the current user's boards
    """
    return self.request.user.boards

  def perform_create(self, serializer):
    """
    Customize the creation of the board so that
    it includes the workspace and the user
    """
    ws = WorkSpace.objects.get(id=self.request.data.get('workspace'))
    serializer.save(workspace=ws, user=self.request.user)

  def destroy(self, request, pk=None):
    """
    Deletes the board with id of pk from 
    the current user
    """
    try:
      board = Board.objects.get(id=int(pk), user=request.user)
      board.delete()
      # Delete the board
      return Response(status=204)
    except:
      return Response({
        'message': 'You are not authorized to delete this'
      }, status=status.HTTP_403_FORBIDDEN)
      


class CardView(ModelViewSet):
  queryset = Card.objects.all()
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = CardSerializer

  def get_queryset(self):
    """
    Return the current user's cards
    """
    return self.request.user.cards

  def perform_create(self, serializer):
    board = Board.objects.get(id=self.request.data.get('board'), user=self.request.user)
    serializer.save(board=board, user=self.request.user)

  
  @action(detail=True, methods=['PATCH'])
  def move(self, request, pk=None):
    """
    Uses the PATCH verb under the path of
    /api/cards/<pk>/move/
    to move the card with id of pk from its current board
    to the board of id of request.data['to']
    """
    to_board_id = request.data['to']
    card = Card.objects.filter(id=pk).first()
    new_board = Board.objects.filter(id=to_board_id).first()

    card.board = new_board
    card.save()

    return Response({ "message": f"Moved to Board '{new_board.name}'" })



class RegisterView(APIView):
    """
    Register an user with an username and password
    """
    def post(self, request):
      username = request.data['username']
      password = request.data['password']
      confirmation = request.data['passwordConfirmation']

      if User.objects.filter(username=username):
        return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

      if password == confirmation:
        user = User.objects.create_user(username=username, password=password)
        user.save()

        return Response({'message': f'User Created {username}'}, status=status.HTTP_201_CREATED)

      return Response({'message': 'error creating user'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
  def post(self, request):
    """
    Logs out the user and deletes the cookies
    from the client
    """
    response = Response()

    # Check if the user is logged in
    if request.COOKIES.get('sessionid'):
      # Delete the token and the session
      response.delete_cookie('access_token')
      response.delete_cookie('sessionid')

      # Delete the refresh token from the session
      request.session = {}

      response.data = { 'message': 'You are logged out' }
      response.status_code = 200
    else:
      # If user is not logged in
      response.data = { 'message': 'You are not logged in' }
      response.status_code = 200
    return response


# Protected API view
class Me(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    # Returns the current user username
    return Response({
      'user': str(request.user)
    })

