from django.urls import path
from . import views

app_name = 'pl_asset'

urlpatterns = [
    path('asset/', views.AssetViewSet.as_list(), name='asset-list'),
    path('asset/<int:pk>', views.AssetViewSet.as_detail(), name='asset-detail'),
]