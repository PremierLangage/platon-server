from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.
class Notification(models.Model):
    """Representation of a `Notification`.

    Attributes:
        name (`str`): Name of the topic.
        desc (`str`): Description of the topic.z
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
    
    
    
    