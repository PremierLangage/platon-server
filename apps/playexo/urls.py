from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'playexo'

urlpatterns = [
    path(
        'play/<int:asset>/',
        views.PlayViewSet.build(),
        name='play-build'
    ),
    path(
        'play/<int:asset>/',
        views.PlayViewSet.eval(),
        name='play-eval'
    ),
    
]
