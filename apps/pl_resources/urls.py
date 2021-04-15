from django.urls import path, include

from . import views

app_name = 'pl_resources'

urlpatterns = [
    path('circles/', views.CircleList.as_view(), name='circle-list'),
    path('circles/<int:pk>/', views.CircleDetail.as_view(), name='circle-detail'),
    path(
        'circles/<int:pk>/resources/',
        views.CircleResourceDetail.as_view(),
        name='circle-resources-detail'
    ),
    path(
        'circles/<int:pk>/tree/',
        views.CircleResourceTree.as_view(),
        name='circle-resources-tree'),

    path('<int:pk>/tag/',views.ResourceTag.as_view(),name='resources-tag'),
    path('<int:pk>/folder/',views.ResourceTag.as_view(),name='resources-folder'),
    path('<int:pk>/folder/',views.ResourceTag.as_view(),name='resources-folder'),

]
