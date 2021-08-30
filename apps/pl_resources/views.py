from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from pl_core.mixins import CrudViewSet
from pl_core.permissions import (AdminOrReadonlyPermission,
                                 AdminOrTeacherPermission)
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from pl_resources.files import Directory

from . import models, permissions, serializers
from .filters import CircleFilter, ResourceFilter

User = get_user_model()


# LEVELS

class LevelListViews(APIView):
    def get(self, request, *args, **kwargs):
        return Response([level.name for level in models.Level.objects.all()])

    def get_permissions(self):
        return [AdminOrReadonlyPermission()]


# TOPICS

class TopicViewSet(CrudViewSet):
    serializer_class = serializers.TopicSerializer
    lookup_field = 'name'
    lookup_url_kwarg = 'name'

    def get_queryset(self):
        return models.Topic.list_all_with_stats().order_by('-references', 'name')

    def get_permissions(self):
        return [AdminOrReadonlyPermission()]


# CIRCLES

class CircleViewSet(CrudViewSet):
    serializer_class = serializers.CircleSerializer

    lookup_field = 'pk'
    lookup_url_kwarg = 'circle_id'

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CircleFilter
    search_fields = [
        'name',
        'topics__name',
        'levels__name'
    ]
    ordering_fields = [
        'watchers_count',
        'members_count',
        'resources_count',
        'updated_at',
        'name'
    ]
    ordering = ['-watchers_count']

    def get_queryset(self):
        return models.Circle.list_all()

    def get_permissions(self):
        return [permissions.CirclePermission()]

    def get_tree(self, request):
        root = models.Circle.find_root()

        def traverse(circle):
            node = {
                'id': circle.pk,
                'name': circle.name,
                'desc': circle.desc,
            }

            children = []
            for child in circle.children.all():
                children.append(
                    traverse(child)
                )

            if len(children):
                node['children'] = children
            return node

        return Response(traverse(root), status=status.HTTP_200_OK)

    def get_completion(self, request):
        query = models.Circle.objects.values_list(
            'name', 'topics', 'levels'
        ).distinct()

        names = set()
        topics = set()
        levels = set()

        for name, topic, level in query:
            names.add(name)
            if topic:
                topics.add(topic)
            if level:
                levels.add(level)

        return Response({
            "names": names,
            "topics": topics,
            "levels": levels
        }, status=status.HTTP_200_OK)

    @classmethod
    def as_tree(cls):
        return cls.as_view({'get': 'get_tree'})

    @classmethod
    def as_completion(cls):
        return cls.as_view({'get': 'get_completion'})


# EVENTS

class EventViewSet(CrudViewSet):
    """The event API provide endpoints to access the events associated to a circle.
    Events are created by the server depending on the activities of the members.
    For example an event will be created when a member is added to the circle.

    Supported methods are the following:

    - `GET` /api/v1/circles/`:circle_id`/events/
    - `GET` /api/v1/circles/`<int:circle_id>`/events/:`<int:event_id>`/
    - `PATCH` /api/v1/circles/`<int:circle_id>`/events/:`<int:event_id>`/
    - `DELETE` /api/v1/circles/`<int:circle_id>`/events/:`<int:event_id>`/
    """

    serializer_class = serializers.EventSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'event_id'

    def get_queryset(self):
        return models.Event.of_circle(
            self.kwargs.get('circle_id')
        ).order_by('-date')

    def get_permissions(self):
        return [permissions.EventPermission()]

    @classmethod
    def as_list(cls):
        return cls.as_view({'get': 'list'})

    @classmethod
    def as_detail(cls):
        return cls.as_view({'get': 'retrieve', 'delete': 'destroy'})


# WATCHERS

class WatcherViewSet(CrudViewSet):
    lookup_field = 'username'
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['username']
    ordering = ['username']

    def get_object(self):
        return self.get_queryset().get(
            username=self.kwargs.get('username'),
        )

    def get_queryset(self):
        return User.objects.filter(
            watched_circles__pk=self.kwargs.get('circle_id')
        )

    def get_permissions(self):
        return [permissions.MemberPermission()]

    def get_serializer_class(self):
        return serializers.WatcherSerializer

    def perform_destroy(self, instance):
        circles = instance.watched_circles
        circle = circles.get(
            pk=self.kwargs.get('circle_id')
        )
        circles.remove(circle)

    def create(self, request, *args, **kwargs):
        circle = models.Circle.objects.get(pk=kwargs.get('circle_id'))
        if circle.watchers.filter(pk=request.user.pk).exists():
            return Response(status=status.HTTP_409_CONFLICT)

        circle.watchers.add(request.user)
        circle.save()

        serializer = self.get_serializer(request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @classmethod
    def as_list(cls):
        return cls.as_view({'get': 'list', 'post': 'create'})

    @classmethod
    def as_detail(cls):
        return cls.as_view({'get': 'retrieve', 'delete': 'destroy'})


# MEMBERS

class MemberViewSet(CrudViewSet):
    serializer_class = serializers.MemberSerializer
    lookup_field = 'user__username'
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email'
    ]
    ordering_fields = ['-date_joined', 'user__username']
    ordering = ['-date_joined', 'user__username']

    def get_object(self):
        return self.get_queryset().get(
            user__username=self.kwargs.get('username'),
        )

    def get_queryset(self):
        return models.Member.objects.filter(
            circle_id=self.kwargs.get('circle_id')
        )

    def get_permissions(self):
        return [permissions.MemberPermission()]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        models.Event.for_member_remove(
            self.request.user,
            instance
        )

    @classmethod
    def as_list(cls):
        return cls.as_view({'get': 'list'})


# INVITATIONS

class InvitationViewSet(CrudViewSet):
    lookup_field = 'invitee__username'
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        'invitee__username',
        'invitee__first_name',
        'invitee__last_name',
        'invitee__email'
    ]
    ordering_fields = ['-date', 'invitee__username']
    ordering = ['-date', 'invitee__username']

    def get_object(self):
        return models.Invitation.objects.get(
            circle__id=self.kwargs.get('circle_id'),
            invitee__username=self.kwargs.get('username'),
        )

    def get_queryset(self):
        return models.Invitation.objects.filter(
            circle_id=self.kwargs.get('circle_id')
        )

    def get_permissions(self):
        return [permissions.MemberPermission()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.InvitationCreateSerializer
        return serializers.InvitationSerializer

    def perform_create(self, serializer):
        serializer.save(
            inviter=self.request.user,
            circle=models.Circle.objects.get(
                pk=self.kwargs.get('circle_id')
            )
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        response = super().destroy(request, *args, **kwargs)
        models.Event.for_member_create(
            instance.inviter,
            models.Member.objects.create(
                user=instance.invitee,
                circle=instance.circle,
                status=instance.status
            )
        )
        return response


# RESOURCES

class ResourceViewSet(CrudViewSet):
    serializer_class = serializers.ResourceSerializer

    lookup_field = 'pk'
    lookup_url_kwarg = 'resource_id'

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ResourceFilter
    search_fields = ['name', 'topics__name', 'levels__name']
    ordering_fields = ['updated_at', 'name']
    ordering = ['-updated_at']

    def get_queryset(self):
        if self.action == 'get_recent_views':
            return models.RecentView.objects.of_user(self.request.user)
        return models.Resource.list_all()

    def get_permissions(self):
        if self.action == 'get_recent_views':
            return [AdminOrTeacherPermission()]
        return [permissions.ResourcePermission()]

    def get_serializer_class(self):
        return serializers.ResourceSerializer

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        Directory.delete(self.kwargs.get('directory'))

    def perform_create(self, serializer):
        super().perform_create(serializer)
        models.Event.for_resource_create(
            self.request.user,
            serializer.instance,
        )

    def perform_update(self, serializer):
        before = self.get_object()
        super().perform_update(serializer)
        after = serializer.instance

        if before.status != after.status:
            models.Event.for_resource_status_change(
                self.request.user,
                after
            )

    def retrieve(self, request, *args, **kwargs):
        models.RecentView.objects.add_item(request.user, self.get_object())
        return super().retrieve(request, *args, **kwargs)

    def get_completion(self, request, *args, **kwargs):
        query = models.Resource.objects.values_list(
            'name', 'topics', 'levels'
        ).distinct()

        names = set()
        topics = set()
        levels = set()

        for name, topic, level in query:
            names.add(name)
            if topic:
                topics.add(topic)
            if level:
                levels.add(level)

        return Response({
            "names": names,
            "topics": topics,
            "levels": levels
        }, status=status.HTTP_200_OK)

    def get_recent_views(self, request, *args, **kwargs):
        self.pagination_class = None
        return self.list(request, *args, **kwargs)

    @classmethod
    def as_completion(cls):
        return cls.as_view({'get': 'get_completion'})

    @classmethod
    def as_recent_views(cls):
        return cls.as_view({'get': 'get_recent_views'})


# FILES

class FileViewSet(CrudViewSet):

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.FileCreateSerializer
        if self.request.method == 'PATCH':
            return serializers.FileRenameSerializer
        if self.request.method == 'PUT':
            return serializers.FileUpdateSerializer
        return None

    def get_permissions(self):
        return [permissions.FilePermission()]

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        path = kwargs.get('path', '.')
        version = query_params.get('version', 'master')

        directory = kwargs.get('directory')
        directory = Directory.get(directory, request.user)

        if 'download' in query_params:
            return directory.download(path, version)

        if 'git-bundle' in query_params:
            return directory.bundle(version)

        if 'git-describe' in query_params:
            return Response({"hash": directory.describe()})

        search = query_params.get('search')
        if search:
            use_regex = query_params.get('use_regex', 'false') == 'true'
            match_word = query_params.get('match_word', 'false') == 'true'
            match_case = query_params.get('match_case', 'false') == 'true'
            return Response(
                directory.search(
                    search,
                    path=path,
                    version=version,
                    match_word=match_word,
                    match_case=match_case,
                    use_regex=use_regex
                )
            )
        return Response(directory.read(path, version, request=request))

    def put(self, request, *args, **kwargs):
        directory = kwargs.get('directory')
        directory = Directory.get(directory, request.user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bundle = serializer.validated_data.get('bundle')
        content = serializer.validated_data.get('content')

        if not bundle and not content:
            return Response(status=status.BAD_REQUEST)

        if content:
            path = kwargs.get('path', '.')
            directory.write_text(path, content)
            return Response(status=status.HTTP_200_OK)

        directory.merge(bundle)
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        directory = kwargs.get('directory')
        directory = Directory.get(directory, request.user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data.get('file')
        files = serializer.validated_data.get('files')

        if file:
            path = self.kwargs.get('path')
            directory.write_file(path, file)
            return Response(status=status.HTTP_201_CREATED)

        if files:
            directory.ignore_commits = True
            for k, v in files.items():
                if v['type'] == 'folder':
                    directory.create_dir(k)
                else:
                    directory.create_file(k, v['content'])
            directory.ignore_commits = False
            directory.commit('create files')
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        path = kwargs.get('path')
        directory = kwargs.get('directory')

        directory = Directory.get(directory, request.user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = serializer.validated_data.get('action')
        newpath = serializer.validated_data.get('newpath')

        if action == "move":
            copy = serializer.validated_data.get('copy')
            directory.move(path, newpath, copy)
            return Response(status=status.HTTP_200_OK)

        if action == 'rename':
            directory.rename(path, newpath)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        path = kwargs.get('path', '.')
        directory = kwargs.get('directory')

        directory = Directory.get(directory, request.user)
        directory.remove(path)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @classmethod
    def as_detail(cls):
        return cls.as_view({
            'get': 'get',
            'patch': 'patch',
            'post': 'post',
            'delete': 'delete'
        })
