from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from pl_core.errors import RestError
from pl_auth.forms import SignInForm

from pl_users.serializers import UserSerializer


class SignInView(APIView):
    """View that handle sign in request."""


    def post(self, request: Request):
        form = SignInForm(request.data)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user is None:
                return Response(
                    RestError('auth/user-not-found'),
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not user.is_active:
                return Response(
                    RestError('auth/user-inactive'),
                    status=status.HTTP_400_BAD_REQUEST
                )

            login(request, user)

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            RestError('validation', form.errors),
            status=status.HTTP_400_BAD_REQUEST
        )


class SignOutView(APIView):
    """View that handle sign out request."""


    def post(self, request: Request):
        # logout session authentifications
        logout(request)

        # TODO blacklist current jwt token
        # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/blacklist_app.html

        return Response({
            'detail': 'successfully logged out'
        }, status=status.HTTP_200_OK)


class MeView(APIView):
    """View that allow to retrieve the logged user's informations"""

    def get(self, request: Request):
        if request.user.is_anonymous:
            return Response(
                RestError('auth/unauthorized'),
                status=status.HTTP_401_UNAUTHORIZED
            )
        serialzer = UserSerializer(request.user)
        return Response(serialzer.data, status=status.HTTP_200_OK)
