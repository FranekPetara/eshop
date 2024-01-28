from django.urls import reverse
from rest_framework import status
import pytest

@pytest.mark.django_db
class TestUserAPI:

    def test_register_valid_user(self, api_client):
        url = reverse('register')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'password123'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {'details': 'User is created'}

    def test_register_existing_user(self, api_client, create_user):
        create_user(email='existinguser@example.com')
        url = reverse('register')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'existinguser@example.com',
            'password': 'password123'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'details': 'User already exists'}

    def test_current_user_authenticated(self, api_client, authenticated_user):
        url = reverse('current_user')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'id': authenticated_user.id, 'first_name': 'John', 'last_name': 'Doe', 'email': 'johndoe@example.com'}

    def test_current_user_unauthenticated(self, api_client):
        url = reverse('current_user')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_user(self, api_client, authenticated_user):
        url = reverse('update_user')
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'janesmith@example.com',
            'password': 'newpassword123'
        }
        response = api_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'id': authenticated_user.id, 'first_name': 'Jane', 'last_name': 'Smith', 'email': 'janesmith@example.com'}

    def test_forgot_password(self, api_client, create_user):
        create_user(email='testuser@example.com')
        url = reverse('forgot_password')
        data = {'email': 'testuser@example.com'}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'email with refresh password was sent to testuser@example.com' in response.data['details']

    def test_reset_password(self, api_client, create_user, create_profile):
        user = create_user()
        profile = create_profile(user=user)
        url = reverse('reset_password', args=[profile.reset_password_token])
        data = {
            'password': 'newpassword123',
            'confirmPassword': 'newpassword123'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'password reset successfully' in response.data['details']

