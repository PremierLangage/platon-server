from django.urls import path

from . import views

app_name = 'pl_auth'

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<str:username>', views.UserDetailView.as_view(), name='user-detail'),
]
