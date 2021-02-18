import django
from django.contrib.auth.models import User

from pl_auth.enums import Role

globals().update(locals())

# Create admin
try:
    user = User.objects.create_user(username='admin', password='adminadmin')
    user.is_staff = True
    user.is_admin = True
    user.is_superuser = True
    user.profile.role = Role.ADMINISTRATOR
    user.save()
except django.db.utils.IntegrityError:
    print("User 'admin' already created")
    pass
