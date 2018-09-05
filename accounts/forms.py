from django import forms
from django.contrib.auth import forms as base_auth_forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from nocaptcha_recaptcha.fields import NoReCaptchaField

from .models import User

CREATE_FIELD_CLASSES = {
    'email': 'uk-input',
    'password1': 'uk-input',
    'password2': 'uk-input',
}

CREATE_FIELD_ICONS = {
    'email': 'fas fa-envelope',
    'password1': 'fas fa-lock',
    'password2': 'fas fa-lock',
}


class UserCreationForm(BaseUserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
    captcha = NoReCaptchaField()

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        # set classes
        for k, v in self.fields.items():
            v.widget.attrs['class'] = CREATE_FIELD_CLASSES.get(k)
            v.widget.icon = CREATE_FIELD_ICONS.get(k)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('email', )


LOGIN_FIELD_CLASSES = {
    'username': 'uk-input',
    'password': 'uk-input',
}

LOGIN_FIELD_ICONS = {
    'username': 'fas fa-envelope',
    'password': 'fas fa-lock',
}


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # set classes
        for k, v in self.fields.items():
            v.widget.attrs['class'] = LOGIN_FIELD_CLASSES.get(k)
            v.widget.icon = LOGIN_FIELD_ICONS.get(k)


SET_PWD_ICONS = {
    'new_password1': 'lock',
    'new_password2': 'lock',
}

SET_PWD_CLASSES = {
    'new_password1': 'uk-input',
    'new_password2': 'uk-input',
}


class SetPasswordForm(base_auth_forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        # set classes
        for k, v in self.fields.items():
            v.widget.attrs['class'] = SET_PWD_CLASSES.get(k)
            v.widget.icon = SET_PWD_ICONS.get(k)
            # remove help text
            if k == 'new_password1':
                v.help_text = None


CONFIRM_PWD_CLASSES = {
    'email': 'uk-input',
}
CONFIRM_PWD_ICONS = {
    'email': 'user',
}


class PasswordResetForm(base_auth_forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        # set classes
        for k, v in self.fields.items():
            v.widget.attrs['class'] = CONFIRM_PWD_CLASSES.get(k)
            v.widget.icon = CONFIRM_PWD_ICONS.get(k)
