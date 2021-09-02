#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  models.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#

from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.db.models.aggregates import Count

from .enums import EventTypes, MemberStatus, ResourceStatus, ResourceTypes

User = get_user_model()


class Topic(models.Model):
    """Representation of a `Topic`.

    Attributes:
        name (`str`): Name of the topic.
        desc (`str`): Description of the topic.
    """

    name = models.CharField(max_length=50, primary_key=True, blank=False)
    desc = models.CharField(max_length=300, blank=True, default='')

    def __str__(self):
        return self.name

    @classmethod
    def list_all_with_stats(cls):
        return Topic.objects.annotate(
            circles_count=Count('circles', distinct=True),
            resources_count=Count('resources', distinct=True),
            references=models.F('circles_count') + models.F('resources_count')
        )


class Level(models.Model):
    """Representation of a `Level`.

    Attributes:
        name (`str`): Name of the Level.
    """

    name = models.CharField(max_length=50, primary_key=True, blank=False)

    def __str__(self):
        return self.name


class Circle(models.Model):
    """Representation of a `Circle`.

    Attributes:
        name (`str`): Name of the circle.
        desc (`str`): Description of the circle.
        opened (`bool`): Indicates whether an invitation is required to add new member.
        updated_at (`datetime`): Update date of the resource.
        created_at (`datetime`): Creation date of the resource.

        parent (`Circle`): Parent of the circle.
        children (`QuerySet`): Children of the circle (related_name in `Circle.parent`).

        topics (`QuerySet`): List of topics associated to the circle.
        levels (`QuerySet`): List of levels associated to the circle.
        watchers (`QuerySet`): List of watchers.

        events (`QuerySet`): Events of the circle (related_name in `Event.circle`).
        resources (`QuerySet`): Resources of the circle (related_name in `Resource.circle`).
        invitations (`QuerySet`): Pending invitations of the circle (related_name in `Invitation.circle`).
    """

    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=300, blank=True, default='Aucune description')
    opened = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    parent = models.ForeignKey(
        'self',
        related_name='children',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    topics = models.ManyToManyField(Topic, related_name='circles', blank=True)
    levels = models.ManyToManyField(Level, related_name='circles', blank=True)
    watchers = models.ManyToManyField(User, related_name='watched_circles', blank=True)


    def __str__(self):
        return self.name

    def is_editable_by(self, user: User) -> bool:
        """Indicates whether the given `user` can edit this circle.
        A circle is editable by an user if:
        - The user is an admin.
        - The user is a member of the circle.
        - The user is an editor and the circle is `opened`.

        Args:
            user (User): An user object.

        Returns:
            bool: `True` if the user can edit the circle `False` otherwise.
        """

        if user.is_admin:
            return True

        if Member.objects.filter(
            user_id=user.id,
            circle_id=self.id,
        ).exists():
            return True

        return user.is_editor and self.opened

    def is_deletable_by(self, user: User) -> bool:
        """Indicates whether the given `user` can delete this circle.
        A circle is detelable by an user if:
        - The user is an admin.

        Args:
            user (User): An user object.

        Returns:
            bool: `True` if the user can delete the circle `False` otherwise.
        """

        return user.is_admin


    @classmethod
    def list_all(cls):
        return cls.__queryset()

    @classmethod
    def find_root(cls):
        return cls.__queryset(parent=None).get()

    @classmethod
    def is_member(cls, user: User, circle_id: int) -> bool:
        if user.is_admin:
            return True

        return Member.objects.filter(
            user_id=user.id,
            circle_id=circle_id,
        ).exists()

    @classmethod
    def __queryset(cls, **kwargs):
        return cls.objects.prefetch_related('topics', 'levels') \
            .filter(**kwargs) \
            .annotate(
                members_count=Count("members", distinct=True),
                children_count=Count("children", distinct=True),
                watchers_count=Count("watchers", distinct=True),
                models_count=Count(
                    "resources",
                    distinct=True,
                    filter=models.Q(resources__type=ResourceTypes.MODEL)
                ),
                exercises_count=Count(
                    "resources",
                    distinct=True,
                    filter=models.Q(resources__type=ResourceTypes.EXERCISE)
                ),
                activities_count=Count(
                    "resources",
                    distinct=True,
                    filter=models.Q(resources__type=ResourceTypes.ACTIVITY)
                ),
                resources_count=(
                    models.F("models_count")
                    + models.F("exercises_count")
                    + models.F("activities_count")
                ),
        )


class Member(models.Model):
    """Representation of an user in a `Circle`.

    Attributes:
        user (`User`): ForeignKey to the `User` model linked to the member.
        circle (`Circle`): ForeignKey to the `Circle` model on which the member belongs to.
        status (`MemberStatus`): Status of the member in the circle.
        date_joined (`datetime`): Date on which the member joined the circle.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    circle = models.ForeignKey(Circle, related_name="members", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=MemberStatus.choices)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'circle'),
        )

    def __str__(self):
        return f'''
            <Member
                name="{self.user.username}"
                circle="{self.circle.name}"
                status="{self.status}"
            >
        '''


class Invitation(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=MemberStatus.choices)
    circle = models.ForeignKey(
        Circle,
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    inviter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    invitee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='circle_invitations',
    )

    class Meta:
        unique_together = (
            ('circle', 'invitee')
        )


    def __str__(self):
        return f'''
        <Invit
            circle="{self.circle.name}"
            status="{self.status}"
            inviter="{self.inviter.username}"
            invitee="{self.invitee.username}"
        >
        '''


class Resource(models.Model):
    """Representation of a resource.

    Args:
        name (`str`): Name of the resource.
        type (`Resource.Types`): Type of the resource.
        desc (`str`): Description of the resource.
        author (`User`): Author of the resource.
        circle (`Circle`): Circle on which the resource belongs to.
        status (`ResourceStatus`): Status of the resource.
        updated_at (`datetime`): Update date of the resource.
        created_at (`datetime`): Creation date of the resource.
        topics (`QuerySet`): List of topics associated to the resource.
        levels (`QuerySet`): List of levels associated to the resource.
    """

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=ResourceTypes.choices)
    desc = models.CharField(max_length=300, blank=True, default='Aucune description')
    status = models.CharField(max_length=20, choices=ResourceStatus.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    topics = models.ManyToManyField(Topic, related_name='resources', blank=True)
    levels = models.ManyToManyField(Level, related_name='resources', blank=True)

    author = models.ForeignKey(User, related_name="resources",  on_delete=models.CASCADE)
    circle: Circle = models.ForeignKey(Circle, related_name="resources", on_delete=models.CASCADE)

    def __str__(self):
        return f'''
            <Resource
                pk={self.pk}
                name="{self.name}"
                type="{self.type}">
        '''

    def is_editable_by(self, user: User) -> bool:
        """Indicates whether the given `user` can edit this resource.
        A resource is editable by an user if:
        - The user is an admin.
        - The user is the author of the resource.
        - The user is an editor and the resource is in a `opened` circle.
        - The user is a member of the circle where the resource is created.

        Args:
            user (User): An user object.

        Returns:
            bool: `True` if the user can edit the resource `False` otherwise.
        """

        if user.is_admin or user.id == self.author_id:
            return True

        if user.is_editor and self.circle.opened:
            return True

        return Member.objects.filter(
            user_id=user.id,
            circle_id=self.circle_id,
        ).exists()


    def is_deletable_by(self, user: User) -> bool:
        """Indicates whether the given `user` can delete this resource.
        A resource is detelable by an user if:
        - The user is an admin.
        - The user is the author of the resource.

        Args:
            user (User): An user object.

        Returns:
            bool: `True` if the user can delete the resource `False` otherwise.
        """

        return user.is_admin or user.id == self.author_id

    @classmethod
    def list_all(cls, *args, **kwargs):
        return Resource.objects.filter(*args, **kwargs)\
            .select_related('author', 'circle')\
            .prefetch_related('topics', 'levels')


class Event(models.Model):
    """Representation of an event in a `Circle`.

    Attributes:
        data (`dict`): Extra informations about the event.
        date (`datetime`): Creation date of the event.
        circle (`Circle`): ForeignKey to the `Circle` model on which the event belongs to.
    """

    type = models.CharField(max_length=50, choices=EventTypes.choices)
    data = models.JSONField(default=dict, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    circle: Circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return f'<Event pk="{self.pk}" type="{self.type}">'

    @classmethod
    def for_member_create(cls, actor: User, member: Member):
        Event.objects.create(
            type=EventTypes.MEMBER_CREATE,
            circle=member.circle,
            data={
                'actor_id': actor.id,
                'actor_name': actor.username,
                'member_id': member.user.id,
                'member_name': member.user.username,
            }
        )

    @classmethod
    def for_member_remove(cls, actor: User, member: Member):
        Event.objects.create(
            type=EventTypes.MEMBER_REMOVE,
            circle=member.circle,
            data={
                'actor_id': actor.id,
                'actor_name': actor.username,
                'member_id': member.user.id,
                'member_name': member.user.username,
            }
        )

    @classmethod
    def for_resource_create(cls, actor: User, resource: Resource):
        Event.objects.create(
            type=EventTypes.RESOURCE_CREATE,
            circle=resource.circle,
            data={
                'actor_id': actor.id,
                'actor_name': actor.username,
                'resource_id': resource.id,
                'resource_name': resource.name,
                'resource_type': resource.type,
            }
        )

    @classmethod
    def for_resource_status_change(cls, actor: User, resource: Resource):
        Event.objects.create(
            type=EventTypes.RESOURCE_STATUS_CHANGE,
            circle=resource.circle,
            data={
                'actor_id': actor.id,
                'actor_name': actor.username,
                'resource_id': resource.id,
                'resource_name': resource.name,
                'resource_type': resource.type,
                'resource_status': resource.status,
            }
        )


    @classmethod
    def of_circle(cls, circle_id: int):
        """List all events in the circle identified by the pk `circle_id`

        Args:
            circle_id (`int`): Identifier of a `Circle`.

        Returns:
            `QuerySet`: A query that resolves with the matched `Event` objects.
        """

        return Event.objects.filter(circle_id=circle_id)


class RecentView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Resource, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date',)  # ordering important
        unique_together = (
            ('user', 'item')
        )

    class QS(models.QuerySet):
        MAX = 10

        @transaction.atomic
        def add_item(self, user, item):
            # to avoid duplicate items
            lrv, created = self.get_or_create(
                user=user,
                item=item,
            )

            if not created:
                lrv.save()  # update timestamp
                return lrv

            self.prune(user)
            return lrv

        def of_user(self, user):
            ids = list(
                self.filter(user=user).values_list('item_id', flat=True)
            )
            # usage of Resource.list_all will include annotations
            return Resource.list_all(id__in=ids)

        def prune(self, user):
            qs = self.filter(user=user)
            if qs.count() > self.MAX:
                pending_delete = qs[self.MAX:]
                self.filter(user=user, pk__in=pending_delete).delete()

    objects = QS.as_manager()

    def __str__(self):
        return f'<RecentView user="{self.user.username}" item="{self.item.name}">'
