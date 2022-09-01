from django.urls import path
from . import views

app_name = 'pl_live'

urlpatterns = [
    path(
        r'live/resource/<int:resource_id>/<uuid:env>',
        views.LiveView.as_view(),
        name='live-session'
    ),
    path(
        'live/resource/<int:resource_id>/',
        views.LiveBuildView.as_view(),
        name='live-build'
    )
]
