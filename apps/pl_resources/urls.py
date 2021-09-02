from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'pl_resources'

urlpatterns = [
    # Levels
    path(
        'levels/',
        views.LevelListViews.as_view(),
        name='level-list'
    ),

    # Topics
    path(
        'topics/',
        views.TopicViewSet.as_list(),
        name='topic-list'
    ),
    path(
        'topics/<str:name>/',
        views.TopicViewSet.as_detail(),
        name='topic-detail'
    ),

    # Circles
    path(
        'circles/',
        views.CircleViewSet.as_list(),
        name='circle-list'
    ),
    path(
        'circles/<int:circle_id>/',
        views.CircleViewSet.as_detail(),
        name='circle-detail'
    ),
    path(
        'circles/tree/',
        views.CircleViewSet.as_tree(),
        name='circle-tree'
    ),
    path(
        'circles/completion/',
        views.CircleViewSet.as_completion(),
        name='circle-completion'
    ),

    # Events
    path(
        'circles/<int:circle_id>/events/',
        views.EventViewSet.as_list(),
        name='circle-event-list'
    ),
    path(
        'circles/<int:circle_id>/events/<int:event_id>/',
        views.EventViewSet.as_detail(),
        name='circle-event-detail'
    ),

    # Members
    path(
        'circles/<int:circle_id>/members/',
        views.MemberViewSet.as_list(),
        name='circle-member-list'
    ),
    path(
        'circles/<int:circle_id>/members/<str:username>/',
        views.MemberViewSet.as_detail(),
        name='circle-member-detail'
    ),

    # Watchers
    path(
        'circles/<int:circle_id>/watchers/',
        views.WatcherViewSet.as_list(),
        name='circle-watcher-list'
    ),
    path(
        'circles/<int:circle_id>/watchers/<str:username>/',
        views.WatcherViewSet.as_detail(),
        name='circle-watcher-detail'
    ),

    # Invitations
    path(
        'circles/<int:circle_id>/invitations/',
        views.InvitationViewSet.as_list(),
        name='circle-invitation-list'
    ),
    path(
        'circles/<int:circle_id>/invitations/<str:username>/',
        views.InvitationViewSet.as_detail(),
        name='circle-invitation-detail'
    ),

    # Resources
    path(
        'resources/',
        views.ResourceViewSet.as_list(),
        name='resource-list'
    ),
    path(
        'resources/completion/',
        views.ResourceViewSet.as_completion(),
        name='resource-completion'
    ),
    path(
        'resources/recent-views/',
        views.ResourceViewSet.as_recent_views(),
        name='resource-recent-views'
    ),
    path(
        'resources/<int:resource_id>/',
        views.ResourceViewSet.as_detail(),
        name='resource-detail'
    ),

    # Files
    url(
        r'files/(?P<directory>(circle|resource):\d+)/(?P<path>[^\?]*)?',
        views.FileViewSet.as_detail(),
        name='files'
    ),
]
