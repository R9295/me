from accounts.models import User
from core.models import Profile
from themes.models import Theme


class TestUtils:

    def _verify_user(self, user):
        user.is_active = True
        user.save()

    def _create_user(self, user=None, verify=True, super_user=False):
        default_user = {
            'email': 'test@asd.asd',
            'password': 'test123456789'
        }
        if user:
            default_user.update(user)
        if super_user:
            user = User.objects.create_superuser(**default_user)
        else:
            user = User.objects.create_user(**default_user)
        if verify:
            self._verify_user(user)
        return user

    def _create_theme(self):
        # this is the ID of the BASIC template
        theme = Theme.objects.create(id='de9d76bb-14fa-45c1-9a99-d01b25414ce8', name='basic')
        return theme

    def _create_profile(self, user=None, profile=None):
        default_profile = {
            'first_name': 'aarnav',
            'last_name': 'bos',
            'description': 'ok',
            'theme': '',
            'user': '',
            'prefix': 'me',
        }
        if profile:
            default_profile.update(profile)
        default_profile['theme'] = self._create_theme()
        if user:
            default_profile['user'] = user
        else:
            default_profile['user'] = self._create_user()
        Profile.objects.create(**default_profile)
