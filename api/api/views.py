from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from api.models import WorkSpace
from api.serializers import *
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.models import User


# The user's login
class CookieObtainTokenPairView(TokenObtainPairView):
  def finalize_response(self, request, response, *args, **kwargs):
    # Check for the 'refresh' key from the response
    if response.data.get('refresh'):
      # 1 day
      # access_max_age = 3600 * 24 * 7
      # Set the cookie
      response.set_cookie('access_token', response.data['access'], max_age=604800, httponly=True, samesite='None', secure=True)

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
    return self.request.user.workspaces
  
  # Return the boards
  def retrieve(self, request, pk=None):
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

  # Return none cards (for now)
  def get_queryset(self):
    return self.request.user.boards

  # Assign the workspace to the board
  def perform_create(self, serializer):
    print(self.request.data.get('workspace'))
    ws = WorkSpace.objects.get(id=self.request.data.get('workspace'))
    serializer.save(workspace=ws, user=self.request.user)

  def destroy(self, request, pk=None):
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
    return self.request.user.cards

  def perform_create(self, serializer):
    board = Board.objects.get(id=self.request.data.get('board'), user=self.request.user)
    serializer.save(board=board, user=self.request.user)

  
  @action(detail=True, methods=['PATCH'])
  def move(self, request, pk=None):
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
      print(request.data)
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
      response.status_code = 401
    return response


# Protected API view
class Me(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    return Response({
      'user': str(request.user)
    })

