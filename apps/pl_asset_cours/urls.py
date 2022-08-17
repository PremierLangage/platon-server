from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'pl_asset_cours'

urlpatterns = [
    path(
        'asset/cours/',
        views.AssetCoursViewSet.as_list(),
        name='cours-list'
    ),
    url(
        r'asset/cours/play/(?P<name>[^\?]*)?/',
        views.AssetCoursSessionViewSet.as_play(),
        name='cours-session'
    ),
    url(
        r'asset/cours/(?P<name>[^\?]*)?/',
        views.AssetCoursViewSet.as_detail(),
        name='cours-detail'
    )
]
