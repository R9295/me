from django.test import Client, TestCase

from .models import User

c = Client()
user = {'email': 'test@asd.asd', 'password1': 'test123456789', 'password2': 'test123456789'}
user_login = {'email': 'test@asd.asd', 'password': 'test123456789'}


class TestAccounts(TestCase):

    def _create_user(self):
        usr = User.objects.create_user(email=user_login['email'], password=user_login['password'])
        return usr

    def test_create_user(self):
        res = c.post('/accounts/signup', user, follow=True)
        self.assertContains(res, 'Thanks for signing up,')

    def test_passwords_not_matching(self):
        _user = user.copy()
        _user['password2'] = 'wrongpassword'
        res = c.post('/accounts/signup', _user, follow=True)
        self.assertContains(res, 'The two password fields didn&#39;t match')

    def test_err_email_exists(self):
        self._create_user()
        res = c.post('/accounts/signup', user, follow=True)
        self.assertContains(res, 'User with this Email address already exists.')

    def test_login(self):
        self._create_user()
        _user = user_login.copy()
        _user['username'] = user_login['email']
        _user.pop('email', None)
        res = c.post('/accounts/login', _user, follow=True)
        # Change this once there's a homepage
        self.assertEqual(res.status_code, 200)
