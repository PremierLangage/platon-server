from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'pl_runner'

urlpatterns = [
    path('runner/', views.RunnerViewSet.as_list(), name='runner-list'),
    path('runner/<int:asset>', views.RunnerViewSet.as_runner(), name='runner-asset'),
    
    url(
        r'runner/live/(?P<directory>(resource):\d+)/',
        views.RunnerViewSet.as_live(),
        name='runner-live'
    ),
]