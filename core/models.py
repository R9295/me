from django.db import models

from accounts.models import User
from themes.models import Theme


def user_image_path(instance, file):
    return 'user_{0}/{1}'.format(instance.user.pk, file)


FEED_TYPES = (
    ('medium', 'Medium'),
    #('FEEDBACK', 'Feedback'),
)


class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to=user_image_path, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True)
    github = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    medium = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    prefix = models.CharField(max_length=25, unique=True)
    short_description = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)
    feed = models.CharField(max_length=15, choices=FEED_TYPES, blank=True)
    # pgp_fingerprint = models.CharField()
    # any key server address(eg. MIT)
    # pgp_link = models.URLField()
