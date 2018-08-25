from django.test import Client, TestCase
from django.urls import reverse

from me.base_tests import TestUtils

from .models import Feedback

c = Client()
user_login = {'email': 'test@asd.asd', 'password': 'test123456789'}


class TestFeedback(TestUtils, TestCase):

        def test_add_feedback(self):
            user = self._create_user()
            c.login(username=user_login['email'], password=user_login['password'])
            c.post(reverse('feedback:add_feedback'), {
                'user': str(user.pk),
                'type': 'FEEDBACK',
                'message': 'MESSAGE123',
                'g-recaptcha-response': 'PASSED',
            }, follow=True)
            self.assertEqual(Feedback.objects.all().count(), 1)

        def test_user_required(self):
            self._create_user()
            c.login(username=user_login['email'], password=user_login['password'])
            res = c.post(reverse('feedback:add_feedback'), {
                'type': 'FEEDBACK',
                'message': 'MESSAGE123',
                'g-recaptcha-response': 'PASSED',
            }, follow=True)
            self.assertContains(res, 'This field is required')

        def test_incorrect_type(self):
            self._create_user()
            c.login(username=user_login['email'], password=user_login['password'])
            res = c.post(reverse('feedback:add_feedback'), {
                'type': '123',
                'message': 'MESSAGE123',
                'g-recaptcha-response': 'PASSED',
            }, follow=True)
            self.assertContains(res, 'Select a valid choice')
