import os
import re

from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.timezone import now

from me.base_tests import TestUtils

from .models import User

c = Client()
user = {'email': 'test@asd.asd', 'password1': 'test123456789', 'password2': 'test123456789'}
user_login = {'email': 'test@asd.asd', 'password': 'test123456789'}


class TestAccounts(TestUtils, TestCase):

    def setUp(self):
        os.environ['NORECAPTCHA_TESTING'] = 'True'

    def test_create_user(self):
        usr = user.copy()
        usr.update({
            'g-recaptcha-response': 'PASSED',
        })
        res = c.post(reverse('accounts:signup'), usr, follow=True)
        self.assertContains(res, 'Thanks for signing up!')
        self.assertEqual(User.objects.all().count(), 1)

    def test_passwords_not_matching(self):
        _user = user.copy()
        _user['password2'] = 'wrongpassword'
        res = c.post(reverse('accounts:signup'), _user, follow=True)
        self.assertContains(res, 'The two password fields didn&#39;t match')

    def test_err_email_exists(self):
        self._create_user()
        res = c.post(reverse('accounts:signup'), user, follow=True)
        self.assertContains(res, 'User with this Email address already exists.')

    def test_login(self):
        user = self._create_user()
        self._verify_user(user)
        _user = user_login.copy()
        _user['username'] = user_login['email']
        _user.pop('email', None)
        res = c.post(reverse('accounts:login'), _user, follow=True)
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
        c.post(reverse('accounts:signup'), usr, follow=True)
        self.assertEqual(len(mail.outbox), 1)

    def test_verify_email_view(self):
        user = self._create_user(verify=False)
        code = user.verification_token
        res = c.get(reverse('accounts:verify', kwargs={'token': code}))
        self.assertEqual(res.status_code, 200)

    def test_404_if_reuse_token(self):
        user = self._create_user(verify=False)
        code = user.verification_token
        c.get(reverse('accounts:verify', kwargs={'token': code}))
        res = c.get(reverse('accounts:verify', kwargs={'token': code}))
        self.assertEqual(res.status_code, 404)

    def test_reset_password(self):
        user = self._create_user()
        password = user.password
        res = c.post(reverse('accounts:password_reset'), {'email': user.email}, follow=True)
        self.assertEqual(len(mail.outbox), 1)
        link = re.search("(?P<url>http?://[^\s]+)", mail.outbox[0].__dict__['body']).group("url")
        reset_link = link[link.find('a')-1:]
        res = c.get(reset_link, follow=True)
        reset_link = res.request['PATH_INFO']
        res = c.post(reset_link, {
            'new_password1': '#1ft32456asda',
            'new_password2': '#1ft32456asda',
        }, follow=True)
        self.assertNotEqual(password, User.objects.first().password)

    def test_reset_password_url_reuse(self):
        user = self._create_user()
        res = c.post(reverse('accounts:password_reset'), {'email': user.email}, follow=True)
        self.assertEqual(len(mail.outbox), 1)
        link = re.search("(?P<url>http?://[^\s]+)", mail.outbox[0].__dict__['body']).group("url")
        reset_link = link[link.find('a')-1:]
        res = c.get(reset_link, follow=True)
        reset_link = res.request['PATH_INFO']
        c.post(reset_link, {
            'new_password1': '#1ft32456asda',
            'new_password2': '#1ft32456asda',
        }, follow=True)
        # re use the url and make sure there is no 'password' in the link
        # password here refers to <input type="password">
        res = c.get(reset_link, follow=True)
        self.assertNotContains(res, 'password')
