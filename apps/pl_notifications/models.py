from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.aggregates import Count

# Create your models here.
class Notification(models.Model):
    """Representation of a `Notification`.

    Attributes:
        type (`str`): Type of the notification.
        user (`User`): The owner of the notification.
        text (str): The description of the notification.
        date (datetime): Creation date of the notification.
        data (dict): extra data on JSON format.    
    """
    type: models.CharField = models.CharField(max_length=20)
    data: models.JSONField = models.JSONField(default=dict, blank=True)
    text: models.TextField = models.TextField(blank=True)
    date: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    user: User = models.ForeignKey(get_user_model(), related_name="notifications_users", on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f'''
            <Notification
                user="{self.user.username}"
                content="{self.text}"
                type="{self.type}"
            >
        '''
    
    @classmethod
    def list_all(cls):
        return Notification.objects\
            .select_related('user')
    
    
    