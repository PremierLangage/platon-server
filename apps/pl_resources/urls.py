from django.urls import path, include

from . import views

app_name = 'pl_resources'

urlpatterns = [

    # Circle's endpoint

    path('circles/', views.CircleList.as_view(), name='circle-list'),
    path('circles/<int:pk>/', views.CircleDetail.as_view(), name='circle-detail'),
    path('circles/<int:pk>/register/', views.CircleRegister.as_view(), name='circle-register'),
    path('circles/<int:pk>/kick/', views.CircleKick.as_view(), name='circle-kick'),
    path('circles/<int:pk>/publish/', views.CirclePublish.as_view(), name='circle-publish'),
    path('circles/<int:pk>/praise/', views.CirclePraise.as_view(), name='circle-praise'),
    path('circles/<int:pk>/blame/', views.CircleBlame.as_view(), name='circle-blame'),
    path('circles/<int:pk>/parents/', views.CircleParents.as_view(), name='circle-parent'),

    # Resource's endpoints

    path('circles/<int:pk>/resources/', views.ResourcesList.as_view(), name='resource-list'),
    path('circles/<int:pk>/resources/<int:pkr>/', views.ResourceDetail.as_view(), name='resource-detail'),
  
    # Version's endpoints

    path('circles/<int:pk>/resources/<int:pkr>/versions/', views.VersionList.as_view(), name='version-list'),
    path('circles/<int:pk>/resources/<int:pkr>/versions/<int:pkv>/', views.VersionDetail.as_view(), name='version-list'),
 

]
