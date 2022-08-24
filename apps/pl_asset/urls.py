from django.urls import path, re_path
from . import views

app_name = 'pl_asset'

urlpatterns = [
    path(
        'asset/',
        views.AssetViewSet.as_list(),
        name='asset-list'
    ),
    path(
        'asset/cours/',
        views.AssetCoursViewSet.as_list(),
        name='asset-cours-list'
    ),
    path(
        'asset/activity/',
        views.AssetActivityViewSet.as_list(),
        name='asset-activity-list'
    ),
    path(
        'asset/exersice/',
        views.AssetExersiceViewSet.as_list(),
        name='asset-exersice-list'
    ),
    re_path(
        r'asset/cours/(?P<name>[^\?]*)?/',
        views.AssetCoursDetailViewSet.as_detail(),
        name='asset-cours-detail'
    ),
    re_path(
        r'asset/activity/(?P<name>[^\?]*)?/',
        views.AssetActivityDetailViewSet.as_detail(),
        name='asset-cours-detail'
    ),
    re_path(
        r'asset/exersice/(?P<name>[^\?]*)?/',
        views.AssetExersiceDetailViewSet.as_detail(),
        name='asset-cours-detail'
    ),
    re_path(
        r'asset/(?P<path>[^\?]*)?/$',
        views.AssetViewSet.as_detail(),
        name='asset-detail'
    ),
]
