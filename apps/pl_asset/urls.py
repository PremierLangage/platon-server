from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'pl_asset'

urlpatterns = [
    # Asset Runner
    path(
        'play/asset/',
        views.RunnableAssetViewSet.as_list(),
        name='playable-list'
    ),
    url(
        r'play/asset/(?P<asset>[^\?]*)?/',
        views.RunnableAssetViewSet.as_detail(),
        name='playable-detail'
    ),

    # Asset
    path(
        'asset/',
        views.AssetViewSet.as_list(),
        name='asset-list'
    ),
    path(
        'asset/me/',
        views.UserAssetViewSet.as_list(),
        name='asset-me'  
    ),
    url(
        r'asset/(?P<path>[^\?]*)?/',
        views.AssetViewSet.as_detail(),
        name='asset-detail'
    )
]
