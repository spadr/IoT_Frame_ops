from django.test import TestCase
from iot.models import User

class UserModelTests(TestCase):

    email = "test1@email.com"
    psw = "test1_passwd"

    def test_user_registration(self):
        user = User.objects.create_user(self.email, self.psw)
        user.is_active = True
        user_registration_was_success = user.save()
        self.assertIs(user_registration_was_success, True)
    
    def test_user_deletion(self):
        user = User.objects.get(self.email, self.psw)
        user_deletion_was_success = user.delete()
        self.assertIs(user_registration_was_success, True)