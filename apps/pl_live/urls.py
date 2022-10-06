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
        name='live-old-build'
    ),
    # NEW
    path(
        'live/build/<int:id>/',
        views.LiveBuild.as_view(),
        name='live-build'
    ),
    path(
        'live/retrieve/<int:id>/<uuid:env>/<path:path>/',
        views.LiveRetrieve.as_view(),
        name='live-retrieve'
    ),
    path(
        'live/grade/<int:id>/<uuid:env>',
        views.LiveGrade.as_view(),
        name='live-grade'
    )
]
