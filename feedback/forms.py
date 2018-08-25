from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField

from .models import Feedback

FIELD_CLASSES = {
    'type': 'uk-select',
    'message': 'uk-textarea',
}


class FeedbackForm(forms.ModelForm):

    captcha = NoReCaptchaField()

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        # set classes
        for k, v in self.fields.items():
            v.widget.attrs['class'] = FIELD_CLASSES.get(k)

    class Meta:
        model = Feedback
        fields = ('user', 'type', 'message')
        widgets = {
            'user': forms.HiddenInput(),
        }
