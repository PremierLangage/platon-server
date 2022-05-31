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

    files_url = serializers.SerializerMethodField(read_only=True)
    events_url = serializers.SerializerMethodField(read_only=True)
    permissions = serializers.SerializerMethodField(read_only=True)
    members_url = serializers.SerializerMethodField(read_only=True)
    watchers_url = serializers.SerializerMethodField(read_only=True)
    resources_url = serializers.SerializerMethodField(read_only=True)
    invitations_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Circle
        exclude = ('watchers',)

    def create(self, validated_data: dict):
        instance = super().create(validated_data)
        request = self.context['request']
        Directory.create(f'circle:{instance.pk}', request.user)
        return instance

    def to_representation(self, value):
        repr = super().to_representation(value)
        if value.parent:
            repr['parent'] = {
                'id': value.parent.id,
                'name': value.parent.name
            }
        return repr

    def get_url(self, value: models.Circle):
        request = self.context['request']
        return reverse(
            'pl_resources:circle-detail',
            request=request,
            kwargs={'circle_id': value.pk}
        )

    def get_files_url(self, value: models.Circle):
        request = self.context['request']
        return reverse(
            'pl_resources:files',
            request=request,
            kwargs={'directory': f'circle:{value.pk}'}
        )

    def get_events_url(self, value: models.Circle):
        request = self.context['request']
        return reverse(
            'pl_resources:circle-event-list',
            request=request,
            kwargs={'circle_id': value.pk}
        )

    def get_permissions(self, value: models.Circle):
        request = self.context['request']
        return {
            'write': value.is_editable_by(request.user),
            'delete': value.is_deletable_by(request.user)
        }

    def get_members_url(self, value: models.Circle):
        request = self.context['request']
        return reverse(
            'pl_resources:circle-member-list',
            request=request,
            kwargs={'circle_id': value.pk}
        )

    def get_watchers_url(self, value: models.Circle):
        request = self.context['request']
        return reverse(
            'pl_resources:circle-watcher-list',
            request=request,
            kwargs={'circle_id': value.pk}
        )

    def get_resources_url(self, value: models.Circle):
        request = self.context['request']
        url = reverse('pl_resources:resource-list', request=request)
        return f'{url}?circle={value.pk}'

    def get_invitations_url(self, value: models.Circle):
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


    def get_url(self, value: models.Event):
        request = self.context['request']
        return reverse(
            'pl_resources:circle-event-detail',
            request=request,
            kwargs={'circle_id': value.circle_id, 'event_id': value.id}
        )


class MemberSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)

    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Member
        fields = ['status', 'username', 'date_joined', 'url']

    def get_url(self, value: models.Member):
        request = self.context['request']
        return reverse(
            'pl_resources:circle-member-detail',
            request=request,
            kwargs={'circle_id': value.circle_id, 'username': value.user}
        )

    def get_username(self, value: models.Member):
        return value.user.username


class WatcherSerializer(UserSerializer):
    username = serializers.CharField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'url']


    def get_url(self, value: User):
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

    def update(self, instance: models.Invitation, validated_data: dict):
        return super().update(instance, validated_data)

    def get_url(self, value: models.Invitation):
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

    def save(self, inviter: User, circle: models.Circle):
        return models.Invitation.objects.create(
            circle=circle,
            inviter=inviter,
            **self.validated_data
        )

    def validate_invitee(self, value: User):
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
    files = serializers.JSONField(required=False, write_only=True)
    files_url = serializers.SerializerMethodField(read_only=True)
    permissions = serializers.SerializerMethodField(read_only=True)
    live_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Resource
        fields = '__all__'
        extra_kwargs = {
            'status': {'default': ResourceStatus.DRAFT},
        }

    def save(self, **kwargs):
        request = self.context['request']
        return super().save(**{'author': request.user, **kwargs})

    def create(self, validated_data: dict):
        files = validated_data.pop('files')
        instance = super().create(validated_data)

        directory = Directory.create(f'resource:{instance.pk}', instance.author)
        if files:
            directory.ignore_commits = True
            for k, v in files.items():
                if v['type'] == 'folder':
                    directory.create_dir(k)
                else:
                    directory.create_file(k, v['content'])
            directory.ignore_commits = False
            directory.commit('create files')
        return instance

    def to_representation(self, value: models.Resource):
        repr = super().to_representation(value)
        repr['circle'] = {
            'id': value.circle.id,
            'name': value.circle.name
        }
        return repr

    def get_url(self, value: models.Resource):
        request = self.context['request']
        return reverse(
            'pl_resources:resource-detail',
            request=request,
            kwargs={'resource_id': value.pk}
        )

    def get_files_url(self, value: models.Resource):
        request = self.context['request']
        return reverse(
            'pl_resources:files',
            request=request,
            kwargs={'directory': f'resource:{value.pk}'}
        )

    def get_permissions(self, value: models.Resource):
        request = self.context['request']
        return {
            'write': value.is_editable_by(request.user),
            'delete': value.is_deletable_by(request.user)
        }
    
    def get_live_url(self, value: models.Resource):
        request = self.context['request']
        return reverse(
            'pl_runner:runner-live',
            request=request,
            kwargs={'directory': f'resource:{value.pk}'}
        )


class FileCreateSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    files = serializers.JSONField(required=False)


class FileRenameSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['move', 'rename'], required=True)
    newpath = serializers.CharField(max_length=100, required=True)
    copy = serializers.BooleanField(required=False)


class FileUpdateSerializer(serializers.Serializer):
    bundle = serializers.FileField(required=False)
    content = serializers.CharField(max_length=134217728, required=False)
