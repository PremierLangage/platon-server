# from asgiref.sync import sync_to_async
# from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import make_password
# from django.urls import reverse

# from channels.testing import WebsocketCommunicator
# from rest_framework import status
# from rest_framework.test import APITestCase

# from .consumers import NotificationConsumer
# from platon.routing import application

# User = get_user_model()


# class NotificationTests(APITestCase):

#     def setUp(self):
#         User.objects.create(username="ypicker", password=make_password("password"))
#         self.user_data = {
#             'username': "ypicker",
#             'password': "password"
#         }
#         self.sign_in_url = reverse('pl_auth:sign-in')
#         return super().setUp()

#     async def test_notification_consumer(self):

#         response = await sync_to_async(self.client.post)(self.sign_in_url, self.user_data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         print(f"response: {response.data}")
#         communicator = WebsocketCommunicator(application.as_asgi(), "ws/notifications/")
#         connected, subprotocol = await communicator.connect()
#         await communicator.send_to(text_data="hello")
#         response = await communicator.receive_from()
#         assert response == "hello"
#         # Close
#         await communicator.disconnect()
