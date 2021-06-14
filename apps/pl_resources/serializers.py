from django.contrib.auth import get_user_model
from django.db import models
from pl_users.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.reverse import reverse

from pl_resources.enums import ResourceStatus

from . import models
from .files import Directory

User = get_user_model()


class TopicSerializer(serializers.ModelSerializer):
    references = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Topic
        fields = '__all__'


class CircleSerializer(serializers.ModelSerializer):
    models_count = serializers.IntegerField(read_only=True, default=0)
    members_count = serializers.IntegerField(read_only=True, default=0)
    watchers_count = serializers.IntegerField(read_only=True, default=0)
    children_count = serializers.IntegerField(read_only=True, default=0)
    exercises_count = serializers.IntegerField(read_only=True, default=0)
    resources_count = serializers.IntegerField(read_only=True, default=0)
    activities_count = serializers.IntegerField(read_only=True, default=0)

    url = serializers.SerializerMethodField(read_only=True)

    events_url = serializers.SerializerMethodField(read_only=True)
    members_url = serializers.SerializerMethodField(read_only=True)
    watchers_url = serializers.SerializerMethodField(read_only=True)
    resources_url = serializers.SerializerMethodField(read_only=True)
    invitations_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Circle
        fields = [
            'id', 'name', 'type', 'parent', 'opened', 'desc', 'topics', 'levels', 'created_at',
            'updated_at', 'children_count', 'watchers_count', 'members_count', 'models_count',
            'exercises_count', 'activities_count', 'resources_count', 'url', 'events_url',
            'members_url', 'watchers_url', 'resources_url', 'invitations_url'
        ]

    def to_representation(self, value):
        repr = super().to_representation(value)
        if value.parent:
            repr['parent'] = {
                'id': value.parent.id,
                'name': value.parent.name
            }
        return repr

    def get_url(self, value):
        request = self.context['request']
        return reverse(
            'pl_resources:circle-detail',
            request=request,
            kwargs={'circle_id': value.pk}
        )

    def get_events_url(self, value):
        request = self.context['request']
        return reverse(
            'pl_resources:circle-event-list',
            request=request,
            kwargs={'circle_id': value.pk}
        )

    def get_members_url(self, value):
        request = self.context['request']
        return reverse(
            'pl_resources:circle-member-list',
            request=request,
            kwargs={'circle_id': value.pk}
        )

    def get_watchers_url(self, value):
        request = self.context['request']
        return reverse(
            'pl_resources:circle-watcher-list',
            request=request,
            kwargs={'circle_id': value.pk}
        )

    def get_resources_url(self, value):
        request = self.context['request']
        url = reverse('pl_resources:resource-list', request=request)
        return f'{url}?circle={value.pk}'

    def get_invitations_url(self, value):
        request = self.context['request']
        return reverse(
            'pl_resources:circle-invitation-list',
            request=request,
            kwargs={'circle_id': value.pk}
        )


class EventSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Event
        fields = ['id', 'type', 'date', 'data', 'url']


    def get_url(self, value):
        request = self.context['request']
        return reverse(
            'pl_resources:circle-event-detail',
            request=request,
            kwargs={'circle_id': value.circle_id, 'event_id': value.id}
        )


class MemberSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username', read_only=True)

    url = serializers.SerializerMethodField(read_only=True)
    circle_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Member
        fields = ['status', 'username', 'date_joined', 'url']

    def get_url(self, value):
        request = self.context['request']
        return reverse(
            'pl_resources:circle-member-detail',
            request=request,
            kwargs={'circle_id': value.circle_id, 'username': value.user}
        )

    def get_username(self, value):
        return value.user.username


class WatcherSerializer(UserSerializer):
    username = serializers.CharField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'url']


    def get_url(self, value):
        kwargs = self.context['view'].kwargs
        request = self.context['request']
        return reverse(
            'pl_resources:circle-watcher-detail',
            request=request,
            kwargs={'circle_id': kwargs.get('circle_id'), 'username': value.username}
        )


class InvitationSerializer(serializers.ModelSerializer):
    inviter = serializers.SlugRelatedField('username', read_only=True)
    invitee = serializers.SlugRelatedField('username', read_only=True)

    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Invitation
        fields = ['inviter', 'invitee', 'date', 'status', 'url']

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def get_url(self, value):
        request = self.context['request']
        return reverse(
            'pl_resources:circle-invitation-detail',
            request=request,
            kwargs={'circle_id': value.circle_id, 'username': value.invitee.username}
        )


class InvitationCreateSerializer(serializers.ModelSerializer):
    invitee = serializers.SlugRelatedField('username', queryset=User.objects.filter())

    class Meta:
        model = models.Invitation
        fields = '__all__'
        extra_kwargs = {
            'circle': {'read_only': True},
            'inviter': {'read_only': True}
        }

    def save(self, inviter, circle):
        return models.Invitation.objects.create(
            circle=circle,
            inviter=inviter,
            **self.validated_data
        )

    def validate_invitee(self, value):
        view = self.context['view']
        request = self.context['request']
        circle_id = view.kwargs.get('circle_id')

        if value is None:
            raise serializers.ValidationError('Required.')

        if value.pk == request.user.id:
            raise serializers.ValidationError('Should be different to "inviter".')

        if value.is_admin:
            raise serializers.ValidationError('Should not be an admin.')

        if not value.is_editor:
            raise serializers.ValidationError('Must be a teacher.')

        query = models.Invitation.objects.filter(
            circle_id=circle_id,
            invitee_id=value.pk,
        )
        if query.exists():
            raise serializers.ValidationError('There is already an invitation sent to this user.')

        query = models.Member.objects.filter(
            circle_id=circle_id,
            user_id=value.pk,
        )
        if query.exists():
            raise serializers.ValidationError('This user is already a member of the circle.')

        return value


class ResourceSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    files_url = serializers.SerializerMethodField(read_only=True)
    versions_url = serializers.SerializerMethodField(read_only=True)
    versions_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = models.Resource
        fields = '__all__'
        extra_kwargs = {
            'status': {'default': ResourceStatus.DRAFT},
        }

    def save(self, **kwargs):
        request = self.context['request']
        return super().save(**{"author": request.user, **kwargs})

    def create(self, validated_data):
        instance = super().create(validated_data)
        Directory.create(instance.pk, instance.author)
        return instance

    def to_representation(self, value):
        repr = super().to_representation(value)
        repr['circle'] = {
            'id': value.circle.id,
            'name': value.circle.name
        }
        return repr

    def get_url(self, value):
        request = self.context['request']
        return reverse(
            'pl_resources:resource-detail',
            request=request,
            kwargs={'resource_id': value.pk}
        )

    def get_files_url(self, value):
        request = self.context['request']
        return reverse(
            'pl_resources:resource-files-master',
            request=request,
            kwargs={'resource_id': value.pk, 'path': ''}
        )

    def get_versions_url(self, value):
        request = self.context['request']
        return reverse(
            'pl_resources:resource-version-list',
            request=request,
            kwargs={'resource_id': value.pk}
        )


class VersionSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField('username', read_only=True)
    number = serializers.IntegerField(read_only=True)

    url = serializers.SerializerMethodField(read_only=True)
    files_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Version
        fields = [
            'number', 'author', 'status', 'message', 'created_at',
            'url', 'files_url',
        ]

    def get_url(self, value):
        view = self.context['view']
        request = self.context['request']
        return reverse(
            'pl_resources:resource-version-detail',
            request=request,
            kwargs={
                'resource_id': view.kwargs.get('resource_id'),
                'version': value.number
            }
        )

    def get_files_url(self, value):
        view = self.context['view']
        request = self.context['request']
        return reverse(
            'pl_resources:resource-version-files',
            request=request,
            kwargs={
                'resource_id': view.kwargs.get('resource_id'),
                'version': value.number,
                'path': ''
            }
        )


class FileCreateSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    files = serializers.JSONField(required=False)


class FileRenameSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['move', 'rename'], required=True)
    newpath = serializers.CharField(max_length=100, required=True)
    copy = serializers.BooleanField(required=False)


class FileUpdateSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=134217728, required=False)
