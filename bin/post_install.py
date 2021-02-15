import random
import string

import django
from django.contrib.auth.models import User

globals().update(locals())

# Create admin
try:
    user = User.objects.create_user(username='admin', password='adminadmin')
    user.is_staff = True
    user.is_admin = True
    user.is_superuser = True
    user.save()
except django.db.utils.IntegrityError:
    print("User 'admin' already created")
    pass

# Create anonymous
try:
    passwd = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    user = User.objects.create_user(username='Anonymous', password=passwd)
    user.save()
except django.db.utils.IntegrityError:
    print("User 'Anonymous' already created")
    pass
