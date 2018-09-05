from dateutil.relativedelta import relativedelta
from django import forms
from django.core.exceptions import ValidationError
from nocaptcha_recaptcha.fields import NoReCaptchaField

from me.base_forms import StyledForm

from .models import Coupon


class CouponActivateForm(StyledForm, forms.Form):
    captcha = NoReCaptchaField()
    code = forms.CharField(max_length=20)

    field_css = {
        'code': 'uk-input'
    }

    field_icons = {
        'code': 'fas fa-unlock'
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CouponActivateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CouponActivateForm, self).clean()
        # raise the error if the captcha is bad before passing through
        if self._errors:
            # small hack here as the error would duplicate otherwise
            errors = self._errors.copy()
            self.__dict__['_errors'] = {}
            raise ValidationError(errors)
        try:
            coupon = Coupon.objects.get(code=cleaned_data.get('code'), activated=False)
            coupon.activated = True
            coupon.activated_by = self.user
            self.user.end_date = self.user.end_date + relativedelta(months=coupon.months)
            coupon.save()
            self.user.save()
        except Coupon.DoesNotExist:
            raise ValidationError({'code': 'Incorrect code'})
