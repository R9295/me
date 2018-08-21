from django.test import Client, TestCase

from accounts.models import User

from .models import Coupon

c = Client()
user = {'email': 'test@asd.asd', 'password1': 'test123456789', 'password2': 'test123456789'}
user_login = {'email': 'test@asd.asd', 'password': 'test123456789'}


class TestCoupon(TestCase):

    def _create_user(self):
        user = User.objects.create_user(**user_login)
        return user

    def _create_superuser(self):
        user = User.objects.create_superuser(**user_login)
        return user

    def test_create_coupon(self):
        self._create_superuser()
        c.login(username=user_login['email'], password=user_login['password'])
        c.post('/admin/coupons/coupon/add/', {
            '_save': ['Save'],
            'activated_by': [''],
            'months': ['12']
        }, follow=True)
        self.assertEqual(Coupon.objects.all().count(), 1)

    def test_activate_coupon(self):
        user = self._create_superuser()
        c.login(username=user_login['email'], password=user_login['password'])
        c.post('/admin/coupons/coupon/add/', {
            '_save': ['Save'],
            'activated_by': [''],
            'months': ['12']
        }, follow=True)
        coupon = Coupon.objects.first()
        end_date = user.end_date
        c.post('/coupons/activate', {'code': coupon.code}, follow=True)
        # check if the end date has increased by 12 months
        diff = User.objects.first().end_date - end_date
        self.assertTrue(367 > diff.days > 364)
        # check if the coupon has expired
        self.assertEqual(Coupon.objects.first().activated, True)
        # check if the user is assigned to acitvated_by
        self.assertEqual(Coupon.objects.first().activated_by, user)
