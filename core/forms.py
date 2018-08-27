from django import forms
from django.core.exceptions import ValidationError

from .models import Profile

FIELD_CLASSES = {
    'prefix': 'uk-input',
    'first_name': 'uk-input',
    'last_name': 'uk-input',
    'short_description': 'uk-input',
    'description': 'uk-textarea',
    'github': 'uk-input',
    'unsplash': 'uk-input',
    'facebook': 'uk-input',
    'twitter': 'uk-input',
    'medium': 'uk-input',
    'linkedin': 'uk-input',
    'theme': 'uk-select',
    'image': 'uk-form-file',
    'feed': 'uk-select',
}

FIELD_ICONS = {
    'prefix': 'home',
    'first_name': 'user',
    'last_name': 'user',
    'short_description': 'info',
    'github': 'github',
    'facebook': 'facebook',
    'twitter': 'twitter',
    'medium': 'medium',
    'linkedin': 'linkedin',
}

# XSS filtering
XSS_FILTERS = [
    'javascript:',
    '.js',
    'document.cookie',
    '.JS',
]


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # set classes
        for k, v in self.fields.items():
            v.widget.attrs['class'] = FIELD_CLASSES.get(k)
            v.widget.icon = FIELD_ICONS.get(k)

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        if 'user' in self.changed_data and self.cleaned_data.get('user'):
            if self.initial['user'] != str(self.cleaned_data.get('user').pk):
                raise ValidationError({'user': "The user you're trying to edit is not you!"})
        for word in XSS_FILTERS:
            if word in self.cleaned_data.get('description'):
                raise ValidationError({'description': 'XSS warning! Nothing related to javascript is allowed'})
        return cleaned_data

    class Meta:
        model = Profile
        fields = ('user', 'prefix', 'image', 'first_name', 'last_name', 'short_description',
                  'description', 'github', 'facebook', 'unsplash',
                  'medium', 'twitter', 'linkedin', 'theme', 'feed', )
        widgets = {
            'user': forms.HiddenInput()
        }
        help_texts = {
            'prefix': 'Your unique url'
        }
