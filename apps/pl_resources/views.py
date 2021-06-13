from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django_filters.rest_framework import DjangoFilterBackend
from pl_core.mixins import CrudViewSet
from pl_core.permissions import AdminOrReadonlyPermission, AdminOrTeacherPermission
from rest_framework import exceptions, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from pl_resources.enums import CircleTypes

from pl_resources.files import Directory

from . import permissions, serializers
from .models import Circle, Event, Invitation, Level, Member, RecentView, Resource, Topic, Version
from .filters import CircleFilter, ResourceFilter

User = get_user_model()


# LEVELS

class LevelListViews(APIView):
    def get(self, request, *args, **kwargs):
        return Response([level.name for level in Level.objects.all()])

    def get_permissions(self):
        return [AdminOrReadonlyPermission()]


# TOPICS

class TopicViewSet(CrudViewSet):
    serializer_class = serializers.TopicSerializer
    lookup_field = 'name'
    lookup_url_kwarg = 'name'

    def get_queryset(self):
        return Topic.list_all_with_stats().order_by('-references', 'name')

    def get_permissions(self):
        return [AdminOrReadonlyPermission()]


# CIRCLES

class CircleViewSet(CrudViewSet):
    serializer_class = serializers.CircleSerializer

    lookup_field = 'pk'
    lookup_url_kwarg = 'circle_id'

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CircleFilter
    search_fields = ['name', 'topics__name', 'levels__name']
    ordering_fields = [
        'watchers_count',
        'members_count',
        'resources_count',
        'updated_at',
        'name'
    ]
    ordering = ['-watchers_count']

    def get_queryset(self):
        if self.action == 'list' and self.request.method == 'GET':
            return Circle.list_publics()
        return Circle.list_all()

    def get_permissions(self):
        return [permissions.CirclePermission()]

    def get_me(self, request):
        circle = Circle.find_personal(request.user)
        serializer = self.get_serializer(circle)
        return Response(serializer.data)

    def get_tree(self, request):
        root = Circle.find_root()

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
        query = Circle.objects.filter(
            type=CircleTypes.PUBLIC
        ).values_list('name', 'topics', 'levels').distinct()

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
        return Event.of_circle(
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


# MEMBERS

class MemberViewSet(CrudViewSet):
    serializer_class = serializers.MemberSerializer
    lookup_field = 'user__username'

    def get_object(self):
        return self.get_queryset().get(
            user__username=self.kwargs.get('username'),
        )

    def get_queryset(self):
        return Member.objects.filter(
            circle_id=self.kwargs.get('circle_id')
        )

    def get_permissions(self):
        return [permissions.MemberPermission()]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        Event.for_member_remove(
            self.request.user,
            instance
        )

    @classmethod
    def as_list(cls):
        return cls.as_view({'get': 'list'})


# WATCHERS

class WatcherViewSet(CrudViewSet):
    lookup_field = 'username'

    def get_object(self):
        return self.get_queryset().get(
            username=self.kwargs.get('username'),
        )

    def get_queryset(self):
        return User.objects.filter(
            watched_circles__pk=self.kwargs.get('circle_id')
        )

    def get_permissions(self):
        return [permissions.WatcherPermission()]

    def get_serializer_class(self):
        return serializers.WatcherSerializer

    def perform_destroy(self, instance):
        circles = instance.watched_circles
        circle = circles.get(pk=self.kwargs.get('circle_id'))
        circles.remove(circle)

    def create(self, request, *args, **kwargs):
        circle = Circle.objects.get(pk=self.kwargs.get('circle_id'))
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


# INVITATIONS

class InvitationViewSet(CrudViewSet):
    lookup_field = 'invitee__username'

    def get_object(self):
        return Invitation.objects.get(
            circle__id=self.kwargs.get('circle_id'),
            invitee__username=self.kwargs.get('username'),
        )

    def get_queryset(self):
        return Invitation.objects.filter(
            circle_id=self.kwargs.get('circle_id')
        )

    def get_permissions(self):
        return [permissions.WatcherPermission()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.InvitationCreateSerializer
        return serializers.InvitationSerializer

    def perform_create(self, serializer):
        serializer.save(
            inviter=self.request.user,
            circle=Circle.objects.get(
                pk=self.kwargs.get('circle_id')
            )
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        response = super().destroy(request, *args, **kwargs)
        Event.for_member_create(
            instance.inviter,
            Member.objects.create(
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
    ordering_fields = ['updated_at', 'name']
    ordering = ['-updated_at']

    def get_queryset(self):
        # TODO remove private resources if no author filter is defined
        return Resource.list_all()

    def get_permissions(self):
        return [permissions.ResourcePermission()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.ResourceCreateSerializer
        return serializers.ResourceSerializer

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        Directory.delete(self.kwargs.get('resource_id'))

    def perform_create(self, serializer):
        super().perform_create(serializer)
        Event.for_resource_create(
            self.request.user,
            serializer.instance,
        )

    def perform_update(self, serializer):
        before = self.get_object()
        super().perform_update(serializer)
        after = serializer.instance

        if before.status != after.status:
            Event.for_resource_status_change(
                self.request.user,
                after
            )

    def retrieve(self, request, *args, **kwargs):
        RecentView.objects.add_item(request.user, self.get_object())
        return super().retrieve(request, *args, **kwargs)

    def get_completion(self, request):
        query = Resource.objects.filter(
            type=CircleTypes.PUBLIC
        ).values_list('name', 'topics', 'levels').distinct()

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


# VERSIONS

class VersionViewSet(CrudViewSet):
    serializer_class = serializers.VersionSerializer

    lookup_field = 'pk'
    lookup_url_kwarg = 'version'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.resource = None

    def get_object(self) -> Version:
        number = self.kwargs.get('version')
        return self.get_queryset().get(number=number)

    def get_queryset(self):
        return Version.of_resource(
            self.resource.pk
        ).order_by('-created_at')

    def get_permissions(self):
        if self.resource is None:
            resource_id = self.kwargs.get('resource_id')
            try:
                self.resource = Resource.objects.get(pk=resource_id)
            except Resource.DoesNotExist:
                raise exceptions.NotFound()
        return [permissions.VersionPermission(self.resource)]

    def perform_create(self, serializer):
        directory = Directory.get(
            self.resource.pk,
            self.request.user
        )

        number = len(directory.versions()) + 1
        version = serializer.save(
            author=self.request.user,
            resource=self.resource,
            number=number
        )

        directory.release(
            f'v{number}',
            version.message
        )

        return version

    @classmethod
    def as_list(cls):
        return cls.as_view({'get': 'list', 'post': 'create'})

    @classmethod
    def as_detail(cls):
        return cls.as_view({'get': 'retrieve', 'patch': 'partial_update'})


# FILES

class FileViewSet(CrudViewSet):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.resource = None

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.FileCreateSerializer

        if self.request.method == 'PATCH':
            return serializers.FileRenameSerializer

        if self.request.method == 'PUT':
            return serializers.FileUpdateSerializer

        return None

    def get_permissions(self):
        if self.resource is None:
            resource_id = self.kwargs.get('resource_id')
            try:
                self.resource = Resource.objects.get(pk=resource_id)
            except Resource.DoesNotExist:
                raise exceptions.NotFound()
        return [permissions.FilePermission(self.resource)]

    def get(self, request, *args, **kwargs):
        return self._handle_get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        path = self.kwargs.get('path')
        resource_id = kwargs.get('resource_id')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data.get('file')
        files = serializer.validated_data.get('files')

        directory = Directory.get(resource_id, request.user)

        if file:
            directory.upload_file(path, file)
            return Response(status=status.HTTP_201_CREATED)

        if files:
            directory.ignore_commits = True
            for k, v in files.items():
                if v["type"] == "file":
                    directory.create_file(k, v["content"])
                else:
                    directory.create_dir(k)
            directory.ignore_commits = False
            directory.commit('batch add files')
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        path = kwargs.get('path')
        resource_id = kwargs.get('resource_id')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        directory = Directory.get(resource_id, request.user)

        action = serializer.validated_data.get('action')
        if action == 'rename':
            directory.rename(
                path,
                serializer.validated_data.get('newpath')
            )
            return Response(status=status.HTTP_200_OK)

        if action == "move":
            directory.move(
                path,
                serializer.validated_data.get('newpath'),
                serializer.validated_data.get('copy')
            )
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        path = self.kwargs.get('path')
        resource_id = self.kwargs.get('resource_id')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        directory = Directory.get(resource_id, request.user)
        directory.write_text(path, serializer.validated_data.get('content'))

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        path = kwargs.get('path')
        resource_id = kwargs.get('resource_id')

        directory = Directory.get(resource_id, request.user)
        directory.remove(path)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def _handle_get(cls, request, *args, **kwargs):
        path = kwargs.get('path', '.')
        version = kwargs.get('version', 'master')
        resource_id = kwargs.get('resource_id')

        if version != 'master':
            version = 'v' + version

        directory = Directory.get(resource_id, request.user)
        if 'download' in request.query_params:
            return directory.download(path, version)

        search = request.query_params.get('search')
        if search:  # search supported only in master
            use_regex = request.query_params.get('use_regex', 'false') == 'true'
            match_word = request.query_params.get('match_word', 'false') == 'true'
            match_case = request.query_params.get('match_case', 'false') == 'true'
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

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def version_files(self, request, *args, **kwargs):
        return self._handle_get(request, *args, **kwargs)

    @classmethod
    def as_master(cls):
        return cls.as_view({
            'get': 'get',
            'patch': 'patch',
            'post': 'post',
            'delete': 'delete'
        })

    @classmethod
    def as_version(cls):
        return cls.as_view({'get': 'version_files'})


# RECENT VIEWS

class RecentViewSet(CrudViewSet):
    serializer_class = serializers.RecentViewSerializer

    def get_queryset(self):
        return RecentView.objects.filter(user=self.request.user)

    def get_permissions(self):
        return [AdminOrTeacherPermission()]
