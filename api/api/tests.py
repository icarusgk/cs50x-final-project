from django.test import TestCase, Client
from django.contrib.auth.models import User

# Create your tests here.

class TestUserAuth(TestCase):
  def setUp(self) -> None:
    self.c = Client()
    self.user = {
      'username': 'test',
      'password': 'test_user'
    }
    User.objects.create_user(**self.user)
    

  def test_user_login(self):
    response = self.c.post('/api/auth/login', self.user)
    # Assert response
    self.assertContains(response, status_code=200, text="{}")

    # Test access token and session id
    self.assertTrue(response.cookies.get('access_token'))
    self.assertTrue(response.cookies.get('sessionid'))


  
  def test_user_logout(self):
    self.test_user_login()
    expected_message = { 'message': 'You are logged out' }
    
    response = self.c.post('/api/auth/logout')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), expected_message)
    
  