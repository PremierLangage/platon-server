from django.urls import path
from . import views

app_name = 'pl_asset'

urlpatterns = [
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
    path(
        'asset/<str:slug_name>/',
        views.AssetViewSet.as_detail(),
        name='asset-detail'
    ),

    # Asset Runner
    path(
        'play/asset',
        views.RunnableAssetViewSet.as_list(),
        name='playable-list'
    ),
    path(
        'play/asset/<str:asset>/',
        views.RunnableAssetViewSet.as_detail(),
        name='playable-detail'
    )
]
