from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'play'

urlpatterns = [
    path(
        'play/<int:asset>/',
        views.PlayViewSet.as_view(),
        name='play'
    ),
]
