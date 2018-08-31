from dateutil.relativedelta import relativedelta
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse_lazy
from django.utils.timezone import now

from me.base_tests import TestUtils

from .models import ProfileAnalytics

user_login = {'email': 'test@asd.asd', 'password': 'test123456789'}
c = Client()


class TestAnalytics(TestUtils, TestCase):

    def test_auto_create_anayltics_instance(self):
        user = self._create_user()
        self._create_profile(user=user)
        self.assertEqual(ProfileAnalytics.objects.all().count(), 1)

    def test_increment(self):
        user = self._create_user()
        profile = self._create_profile(user=user)
        c.get(reverse_lazy('analytics:increment', kwargs={
            'profile_id': str(profile.pk),
            'platform': 'twitter'
        })+'?redir='+'https://twitter.com/aarnavrotten')
        self.assertEqual(ProfileAnalytics.objects.get(profile=profile.pk).twitter_visits, 1)

    def test_clear_analytics_month_end(self):
        user = self._create_user()
        profile = self._create_profile(user=user)
        a = ProfileAnalytics.objects.get(profile=profile.pk)
        a.last_updated = now() - relativedelta(months=1)
        a.profile_visits = 5
        a.save()
        call_command('reset_analytics')
        self.assertEqual(ProfileAnalytics.objects.get(profile=profile.pk).profile_visits, 0)

    def test_analytics_page(self):
        user = self._create_user()
        profile = self._create_profile(user=user, profile={
            'twitter': 'https://twitter.com/aarnavrotten'
        })
        c.get(reverse_lazy('analytics:increment', kwargs={
            'profile_id': str(profile.pk),
            'platform': 'twitter'
        })+'?redir='+'https://twitter.com/aarnavrotten')
        c.login(username=user_login['email'], password=user_login['password'])
        res = c.get(reverse_lazy('analytics:analytics_user'))
        self.assertContains(res, 'Twitter</h3>\n      <p>1</p>')
