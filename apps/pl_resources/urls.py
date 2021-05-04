from django.urls import path, include

from . import views

app_name = 'pl_resources'

urlpatterns = [
    
    path('', views.ResourcesList.as_view(), name='resources-list'),
    path('<int:pk>/', views.ResourceDetail.as_view(), name='resources-detail'),
    
    path('<int:pk>/files/', views.FileList.as_view(), name='files-list'),
    path('<int:pk>/files/<int:fpk>/', views.FileDetail.as_view(), name='files-detail'),

    # Circle
    path('circles/', views.CircleList.as_view(), name='circle-list'),
    path('circles/<int:pk>/', views.CircleDetail.as_view(), name='circle-detail'),
    path(
        'circles/<int:pk>/tree/',
        views.CircleResourceTree.as_view(),
        name='circle-resources-tree'),


    # New Endpoints

    # Circle's endpoint

    path('circles/', views.CircleList.as_view(), name='circle-list'),
    path('circles/<int:pk>/', views.CircleDetail.as_view(), name='circle-detail'),
    path('circles/<int:pk>/register/', views.CircleDetail.as_view(), name='circle-detail'),
    path('circles/<int:pk>/kick/', views.CircleDetail.as_view(), name='circle-detail'),
    path('circles/<int:pk>/publish/', views.CircleDetail.as_view(), name='circle-detail'),
    path('circles/<int:pk>/praise/', views.CircleDetail.as_view(), name='circle-detail'),
    path('circles/<int:pk>/blame/', views.CircleDetail.as_view(), name='circle-detail'),
    path('circles/<int:pk>/parent/', views.CircleDetail.as_view(), name='circle-detail'),

    # Resource's endpoints

    path('circles/<int:pk>/resources/', views.ResourcesList.as_view(), name='resource-list'),
    path('circles/<int:pk>/resources/<int:pkr>/', views.ResourcesList.as_view(), name='resource-list'),
  
    # Version's endpoints

    path('circles/<int:pk>/resources/<int:pkr>/versions/', views.ResourcesList.as_view(), name='resource-list'),
    path('circles/<int:pk>/resources/<int:pkr>/versions/<int:pkv>/', views.ResourcesList.as_view(), name='resource-list'),
 

]
