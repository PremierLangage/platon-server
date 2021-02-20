from django.urls import path, include

from . import views

app_name = 'pl_lti'

urlpatterns = [
    path('info/', views.InfoView.as_view(), name='info'),
]
