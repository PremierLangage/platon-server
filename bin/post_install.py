import django
from django.contrib.auth.models import User

from pl_auth.enums import Role
from pl_lti.models import LMS

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

# Create UPEM Elearning LMS
try:
    LMS.objects.create(
        guid="elearning.u-pem.fr",
        name="ELEARNING UPEM",
        url="https://elearning.u-pem.fr/",
        outcome_url="https://elearning.u-pem.fr/mod/lti/service.php",
        client_id="moodle",
        client_secret="secret"
    )
except django.db.utils.IntegrityError:
    print("LMS 'ELEARNING UPEM' already created")
    pass
