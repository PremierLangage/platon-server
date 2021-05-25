from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'pl_auth'

urlpatterns = [
    path('auth/sign-in/', TokenObtainPairView.as_view(), name='sign-in'),
    path('auth/sign-out/', views.SignOutView.as_view(), name='sign-out'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh'),
]
