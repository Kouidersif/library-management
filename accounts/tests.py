from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class AccountsTests(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.refresh_url = reverse('accounts:refresh')
        
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        self.login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }

    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')
        
    def test_user_registration_invalid_data(self):
        """Test user registration with invalid data"""
        # Test with mismatched passwords
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'wrongpass'
        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test with existing email
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        """Test user login"""
        # Create a user first
        self.client.post(self.register_url, self.user_data, format='json')
        
        # Test login
        response = self.client.post(self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn('refresh', response_data)
        self.assertIn('access', response_data)

    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials"""
        # Create a user first
        self.client.post(self.register_url, self.user_data, format='json')
        
        # Test with wrong password
        invalid_login = self.login_data.copy()
        invalid_login['password'] = 'wrongpass'
        response = self.client.post(self.login_url, invalid_login, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_logout(self):
        """Test user logout"""
        # Create and login user
        self.client.post(self.register_url, self.user_data, format='json')
        login_response = self.client.post(self.login_url, self.login_data, format='json')
        
        # Test logout
        login_data = login_response.json()
        logout_data = {'refresh': login_data['refresh']}
        response = self.client.post(
            self.logout_url,
            logout_data,
            format="json",
            headers={"Authorization": f"Bearer {login_data['access']}"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_refresh(self):
        """Test token refresh"""
        # Create and login user
        self.client.post(self.register_url, self.user_data, format='json')
        login_response = self.client.post(self.login_url, self.login_data, format='json')
        login_data = login_response.json()
        
        # Test token refresh
        refresh_data = {'refresh': login_data['refresh']}
        response = self.client.post(self.refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn('access', response_data)

    def test_token_refresh_invalid_token(self):
        """Test token refresh with invalid token"""
        refresh_data = {'refresh': 'invalid-token'}
        response = self.client.post(self.refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
