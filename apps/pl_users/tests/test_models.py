from django.contrib.auth import get_user_model
from django.test import TestCase
from pl_lti.role import Role

User = get_user_model()


class ModelsTestCase(TestCase):
    """ Test functions of pl_users.models modules. """


    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user', password='12345', id=100)


    def test_is_admin(self):
        self.user.is_staff = False
        self.user.is_superuser = False
        self.assertFalse(self.user.is_admin)

        self.user.is_staff = True
        self.assertTrue(self.user.is_admin)

        self.user.is_staff = False
        self.user.is_superuser = True
        self.assertTrue(self.user.is_admin)
