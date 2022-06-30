from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'pl_loader'

urlpatterns = [
    
    # Loader
    url(
        r'loader/(?P<directory>(resource):\d+)/',
        views.LoaderViewSet.as_load(),
        name='loader'
    ),

    # Publisher
    url(
        r'publisher/(?P<directory>(resource):\d+)/',
        views.PublisherViewSet.as_publish(),
        name='publisher'
    ),
]

