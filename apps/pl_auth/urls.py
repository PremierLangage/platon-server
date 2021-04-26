from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'pl_auth'

urlpatterns = [
    path('signin/', TokenObtainPairView.as_view(), name='signin'),
    path('signout/', views.SignOutView.as_view(), name='signout'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('user/', views.LoggedUserDetailView.as_view(), name='logged-user'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<str:username>', views.UserDetailView.as_view(), name='user-detail'),
]
