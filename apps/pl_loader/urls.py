from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'pl_loader'

urlpatterns = [
    # Publisher
    url(
        r'loader/(?P<directory>(resource):\d+)/',
        views.Publisher.as_detail(),
        name='publisher'
    )
]

