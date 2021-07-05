import json

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken



User = get_user_model()


class AuthTestCase(APITestCase):

    def setUp(self):
        User.objects.create(username="ypicker", password=make_password("password"))
        self.user_data = {
            'username': "ypicker",
            'password': "password"
        }
        self.sign_in_url = reverse('pl_auth:sign-in')
        return super().setUp()

    def test_force_authenticate(self):
        user = User.objects.get(username='ypicker')
        client = APIClient()
        client.force_authenticate(user=user)

    def user_cannot_sign_in_with_no_data(self):
        response = self.client.post(self.sign_in_url)
        return self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_authenticate(self):
        response = self.client.post(self.sign_in_url, self.user_data)
        return self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_authenticate_with_bad_password(self):
        bad_data_connection = {
            'username': "ypicker",
            'password': "bad_password"
        }
        response = self.client.post(self.sign_in_url, bad_data_connection)
        return self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)