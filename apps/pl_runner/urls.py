from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'pl_runner'

urlpatterns = [
    url(
        r'runner/(?P<directory>(circle|resource):\d+)/(?P<path>[^\?]+)?',
        views.Loader.as_view(),
        name='runner'
    ),
]