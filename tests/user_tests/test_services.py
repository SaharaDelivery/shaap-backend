from django.test import TestCase
from django.utils import timezone

from users.models import CustomUser
from users.services import (
    create_user,
    disable_user_account,
    edit_user_account,
    login_user,
)

from tests.user_tests.serializers import UserSerializer


class ServicesTest(TestCase):
    def setUp(self):
        self.user_dict = {
            "first_name": "user-first",
            "last_name": "user-last",
            "username": "user",
            "email": "user@user.com",
            "phone_number": "12345678912",
            "password": "user",
        }
        self.user = create_user(data=self.user_dict)

    def test_create_user(self):
        data = UserSerializer(self.user)
        password = self.user_dict.pop("password")
        self.assertTrue(self.user.check_password(password))
        self.assertEqual(data.data, self.user_dict)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_driver)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_admin)
        self.assertFalse(self.user.is_superuser)

    def test_edit_user_account(self):
        edit_dict = {
            "first_name": "edited-first",
            "last_name": "edited-last",
            "username": "edited-user",
            "email": "edited-user@user.com",
            "phone_number": "00000000000",
        }
        # NOTE: This object is the same as the self.user but i renamed it so itll be better to understand
        edited_user = edit_user_account(user=self.user, data=edit_dict)
        data = UserSerializer(edited_user)
        self.assertEqual(data.data, edit_dict)
        self.assertTrue(edited_user.is_active)
        self.assertFalse(edited_user.is_staff)
        self.assertFalse(edited_user.is_driver)
        self.assertFalse(edited_user.is_staff)
        self.assertFalse(edited_user.is_admin)
        self.assertFalse(edited_user.is_superuser)

    def test_user_login(self):
        now = timezone.now()
        user = login_user(user=self.user)
        self.assertAlmostEqual(now, user.last_login)

    def test_disable_user_account(self):
        disable_user_account(user=self.user)
        self.assertFalse(self.user.is_active)
