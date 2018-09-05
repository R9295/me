from django import forms
from django.core.exceptions import ValidationError

from me.base_forms import StyledForm

from .models import Profile

# XSS filtering
XSS_FILTERS = [
    'javascript:',
    '.js',
    'document.cookie',
    '.JS',
]


class ProfileForm(StyledForm, forms.ModelForm):
    field_css = {
        'prefix': 'uk-input',
        'first_name': 'uk-input',
        'last_name': 'uk-input',
        'short_description': 'uk-input',
        'description': 'uk-textarea',
        'github': 'uk-input',
        'facebook': 'uk-input',
        'twitter': 'uk-input',
        'medium': 'uk-input',
        'linkedin': 'uk-input',
        'unsplash': 'uk-input',
        'theme': 'uk-select',
        'image': 'uk-form-file',
    }

    field_icons = {
        'prefix': 'fas fa-home',
        'first_name': 'far fa-user',
        'last_name': 'far fa-user',
        'short_description': 'fas fa-info-circle',
        'github': 'fab fa-github',
        'facebook': 'fab fa-facebook',
        'twitter': 'fab fa-twitter',
        'medium': 'fab fa-medium',
        'linkedin': 'fab fa-linkedin',
        'unsplash': 'fab fa-unsplash',
    }

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
                  'medium', 'twitter', 'linkedin', 'theme',)
        widgets = {
            'user': forms.HiddenInput()
        }
        help_texts = {
            'prefix': 'Your unique url'
        }
