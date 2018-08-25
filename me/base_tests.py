from accounts.models import User


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
