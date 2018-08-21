from django.db import models
from django.utils.crypto import get_random_string
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta


def get_rand_string():
    string = get_random_string(20)
    return string


def get_expiry_date():
    date = now() + relativedelta(months=1)
    return date


class Coupon(models.Model):

    activated = models.BooleanField(default=False)
    code = models.CharField(default=get_rand_string, unique=True, max_length=20, editable=False)
    activated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                                     blank=True, default=None)
    months = models.IntegerField(validators=[MinValueValidator(1),
                                 MaxValueValidator(12)])
    expires = models.DateTimeField(default=get_expiry_date, editable=False)

    def __str__(self):
        return self.code
