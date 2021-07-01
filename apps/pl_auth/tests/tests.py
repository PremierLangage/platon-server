from django.contrib.auth import get_user_model, authenticate, login, logout

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


User = get_user_model()


class AuthTestCase(APITestCase):

    def setUp(self):
        User.objects.create(username="ypicker", password="password")
        User.objects.create(username="zpicker", password="password")


    def test_force_authenticate(self):
        user = User.objects.get(username='ypicker')
        client = APIClient()
        client.force_authenticate(user=user)
        
    def test_simple_authenticate(self):
        user = authenticate(username='ypicker', password='password')
        client = APIClient()
        client.login(username='lauren', password='secret')



    def test_get_token(self):
        url = reverse('pl_auth:sign-in')
        data = {'username': 'yicker', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)