from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.aggregates import Count

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your models here.


class Notification(models.Model):
    """Representation of a `Notification`.

    Attributes:
        type (`str`): Type of the notification.
        user (`User`): The owner of the notification.
        date (datetime): Creation date of the notification.
        data (dict): extra data on JSON format.
    """

    type: models.CharField = models.CharField(max_length=20)
    data: models.JSONField = models.JSONField(default=dict, blank=True)
    date: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    user: User = models.ForeignKey(get_user_model(), related_name="notifications_users", on_delete=models.CASCADE)


    def __str__(self):
        return f'''
            <Notification
                user="{self.user.username}"
                type="{self.type}"
            >
        '''

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(self.user.username, {
            "type": "notification.message",
            "text": "Notifications are available now.",
        })
        super(self).save(*args, **kwargs)

    @classmethod
    def list_all(cls):
        return Notification.objects\
            .select_related('user')
