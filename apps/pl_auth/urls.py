from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'pl_auth'

urlpatterns = [
    path('me/', views.MeView.as_view(), name='me'),
    path('sign-in/', TokenObtainPairView.as_view(), name='sign-in'),
    path('sign-out/', views.SignOutView.as_view(), name='sign-out'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
]
