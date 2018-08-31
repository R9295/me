from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.timezone import now

from accounts.models import User
from core.models import Profile
from me.base_tests import TestUtils
from themes.models import Theme

c = Client()
user = {'email': 'test@asd.asd', 'password1': 'test123456789', 'password2': 'test123456789'}
user_login = {'email': 'test@asd.asd', 'password': 'test123456789'}


class TestCore(TestUtils, TestCase):
    def setUp(self):
        self.profile = {
            'first_name': 'aarnav',
            'last_name': 'bos',
            'description': 'ok',
            'theme': '',
            'user': '',
            'prefix': 'me',
        }

    def test_create_profile(self):
        _user = self._create_user()
        theme = self._create_theme()
        profile = self.profile.copy()
        profile['theme'] = theme.pk
        profile['user'] = str(_user.pk)
        c.login(username=user_login['email'], password=user_login['password'])
        c.post(reverse('core:profile'), profile, follow=True)
        self.assertEqual(Profile.objects.all().count(), 1)

    def test_prefix_exists(self):
        self._create_profile()
        _user = self._create_user(user={'email': 'test@asd1.asd', 'password': 'test123456789'})
        profile = self.profile.copy()
        profile['theme'] = Theme.objects.first().pk
        profile['user'] = str(_user.pk)
        c.login(username='test@asd1.asd', password='test123456789')
        res = c.post(reverse('core:profile'), profile, follow=True)
        self.assertContains(res, 'Profile with this Prefix already exists.')

    def test_user_is_not_you(self):
        _user = self._create_user()
        theme = self._create_theme()
        self._create_user(user={'email': 'test@asd1.asd', 'password': 'test123456789'})
        profile = self.profile.copy()
        profile['theme'] = theme.pk
        profile['user'] = str(_user.pk)
        c.login(username='test@asd1.asd', password='test123456789')
        res = c.post(reverse('core:profile'), profile, follow=True)
        self.assertContains(res, "The user you&#39;re trying to edit is not you!")

    def test_user_required(self):
        self._create_user()
        theme = self._create_theme()
        profile = self.profile.copy()
        profile.pop('user', None)
        profile['theme'] = theme.pk
        c.login(username='test@asd.asd', password='test123456789')
        res = c.post(reverse('core:profile'), profile, follow=True)
        self.assertContains(res, "This field is required.")

    def test_theme_required(self):
        _user = self._create_user()
        self._create_theme()
        profile = self.profile.copy()
        profile.pop('theme', None)
        profile['user'] = _user.pk
        c.login(username='test@asd.asd', password='test123456789')
        res = c.post(reverse('core:profile'), profile, follow=True)
        self.assertContains(res, 'This field is required')

    def test_prefix_required(self):
        _user = self._create_user()
        theme = self._create_theme()
        profile = self.profile.copy()
        profile['theme'] = theme.pk
        profile['user'] = str(_user.pk)
        profile.pop('prefix', None)
        c.login(username=user_login['email'], password=user_login['password'])
        res = c.post(reverse('core:profile'), profile, follow=True)
        self.assertContains(res, 'This field is required')

    def test_markdown_xss(self):
        _user = self._create_user()
        theme = self._create_theme()
        c.login(username=user_login['email'], password=user_login['password'])
        profile = self.profile.copy()
        profile['theme'] = theme.pk
        profile['user'] = str(_user.pk)
        profile['description'] = '[](javascript:alert(123))>'
        res = c.post(reverse('core:profile'), profile, follow=True)
        self.assertContains(res, 'XSS warning!')
        profile['description'] = '[](http://someserver/somescript.js)'
        res = c.post(reverse('core:profile'), profile, follow=True)
        self.assertContains(res, 'XSS warning!')
        profile['description'] = '[](http://someserver/somescript.JS)'
        res = c.post(reverse('core:profile'), profile, follow=True)
        self.assertContains(res, 'XSS warning!')

    def test_inactive_profile(self):
        user = User.objects.create_user(email=user_login['email'],
                                        password=user_login['password'],
                                        end_date=now()-relativedelta(months=1))
        self._create_profile(user=user)
        call_command('check_end_date')
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.active, False)

    def test_404_if_inactive_profile(self):
        user = self._create_user({'end_date': now()-relativedelta(months=1)})
        self._create_profile(user=user)
        res = c.get(reverse('core:user', kwargs={'user_prefix': 'me'}), follow=True)
        self.assertEqual(res.status_code, 200)
        call_command('check_end_date')
        res = c.get(reverse('core:user', kwargs={'user_prefix': 'me'}), follow=True)
        self.assertEqual(res.status_code, 404)

    def test_image_field(self):
        _user = self._create_user()
        theme = self._create_theme()
        profile = self.profile.copy()
        profile['theme'] = theme.pk
        profile['user'] = str(_user.pk)
        with open(settings.BASE_DIR+'/media/defaults/default_user.png', 'rb') as img:
            profile['image'] = img
            c.login(username=user_login['email'], password=user_login['password'])
            c.post(reverse('core:profile'), profile, follow=True)
            self.assertNotEqual(Profile.objects.first().image, None)
