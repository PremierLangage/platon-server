from django.urls import path, include

from . import views

app_name = 'pl_resources'

urlpatterns = [
    path('circles/', views.CircleList.as_view(), name='circle-list'),
    path('circles/<int:pk>/', views.CircleDetail.as_view(), name='circle-detail'),
    path(
        'circles/<int:pk>/tree/',
        views.CircleResourceTree.as_view(),
        name='circle-resources-tree'),

    path('',views.ResourcesList.as_view(), name='resources-list'),
    path('<int:pk>/',views.ResourceDetail.as_view(), name='resources-detail'),
    path('<int:pk>/tag/',views.ResourceTag.as_view(),name='resources-tag'),
    path('<int:pk>/folder/',views.ResourceFolder.as_view(),name='resources-folder'),
    
    path('<int:pk>/files/',views.FilesList.as_view(), name='files-list'),
    path('<int:pk>/files/<int:fpk>/',views.FileDetail.as_view(), name='files-detail'),


]
