from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField
from me.base_forms import StyledForm
from .models import Feedback


class FeedbackForm(StyledForm, forms.ModelForm):
    field_css = {
        'type': 'uk-select',
        'message': 'uk-textarea',
    }
    field_icons = None
    captcha = NoReCaptchaField()

    class Meta:
        model = Feedback
        fields = ('user', 'type', 'message')
        widgets = {
            'user': forms.HiddenInput(),
        }
