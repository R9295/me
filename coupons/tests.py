import os

from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import User
from me.base_tests import TestUtils

from .models import Coupon

c = Client()
user = {'email': 'test@asd.asd', 'password1': 'test123456789', 'password2': 'test123456789'}
user_login = {'email': 'test@asd.asd', 'password': 'test123456789'}


class TestCoupon(TestUtils, TestCase):

    def setUp(self):
        os.environ['NORECAPTCHA_TESTING'] = 'True'

    def test_create_coupon(self):
        self._create_user(super_user=True)
        c.login(username=user_login['email'], password=user_login['password'])
        c.post(reverse('admin:coupons_coupon_add'), {
            '_save': ['Save'],
            'activated_by': [''],
            'months': ['12']
        }, follow=True)
        self.assertEqual(Coupon.objects.all().count(), 1)

    def test_activate_coupon(self):
        user = self._create_user(super_user=True)
        c.login(username=user_login['email'], password=user_login['password'])
        c.post(reverse('admin:coupons_coupon_add'), {
            '_save': ['Save'],
            'activated_by': [''],
            'months': ['12']
        }, follow=True)
        coupon = Coupon.objects.first()
        end_date = user.end_date
        c.post(reverse('coupons:activate'), {'code': coupon.code,
                                             'g-recaptcha-response': 'PASSED'},
               follow=True)
        # check if the end date has increased by 12 months
        diff = User.objects.first().end_date - end_date
        self.assertTrue(367 > diff.days > 364)
        # check if the coupon has expired
        self.assertEqual(Coupon.objects.first().activated, True)
        # check if the user is assigned to acitvated_by
        self.assertEqual(Coupon.objects.first().activated_by, user)

    def test_cannot_edit_coupon(self):
        self._create_user(super_user=True)
        c.login(username=user_login['email'], password=user_login['password'])
        c.post(reverse('admin:coupons_coupon_add'), {
            '_save': ['Save'],
            'activated_by': [''],
            'months': ['12']
        }, follow=True)
        self.assertEqual(Coupon.objects.all().count(), 1)
        coupon = Coupon.objects.first()
        c.post(reverse('admin:coupons_coupon_change', kwargs={'object_id': str(coupon.pk)}), {
            '_save': ['Save'],
            'activated_by': ['123'],
            'months': ['6']
        }, follow=True)
        self.assertEqual(Coupon.objects.first().months, 12)
