import os

from django.core import mail
from django.test import Client, TestCase
from django.utils.timezone import now

from .models import User

c = Client()
user = {'email': 'test@asd.asd', 'password1': 'test123456789', 'password2': 'test123456789'}
user_login = {'email': 'test@asd.asd', 'password': 'test123456789'}


class TestAccounts(TestCase):

    def setUp(self):
        os.environ['NORECAPTCHA_TESTING'] = 'True'

    def _verify_user(self, user):
        user.is_active = True
        user.save()

    def _create_user(self):
        usr = User.objects.create_user(email=user_login['email'], password=user_login['password'])
        return usr

    def test_create_user(self):
        usr = user.copy()
        usr.update({
            'g-recaptcha-response': 'PASSED',
        })
        res = c.post('/accounts/signup', usr, follow=True)
        self.assertContains(res, 'Thanks for signing up!')
        self.assertEqual(User.objects.all().count(), 1)

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
        user = self._create_user()
        self._verify_user(user)
        _user = user_login.copy()
        _user['username'] = user_login['email']
        _user.pop('email', None)
        res = c.post('/accounts/login', _user, follow=True)
        # Change this once there's a homepage
        self.assertEqual(res.status_code, 200)

    def test_end_date(self):
        user = self._create_user()
        diff = user.end_date - now()
        diff = 32 > int(diff.days) > 28
        self.assertTrue(diff)

    def test_email_verify_message(self):
        usr = user.copy()
        usr.update({
            'g-recaptcha-response': 'PASSED',
        })
        c.post('/accounts/signup', usr, follow=True)
        self.assertEqual(len(mail.outbox), 1)

    def test_verify_email_view(self):
        user = self._create_user()
        code = user.verification_token
        res = c.get('/accounts/verify/{}'.format(code))
        self.assertEqual(res.status_code, 200)

    def test_404_if_reuse_token(self):
        user = self._create_user()
        code = user.verification_token
        c.get('/accounts/verify/{}'.format(code))
        res = c.get('/accounts/verify/{}'.format(code))
        self.assertEqual(res.status_code, 404)
