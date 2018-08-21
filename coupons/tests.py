from django.test import TestCase, Client
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
