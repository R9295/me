from django.db import models
from django.utils.timezone import now

from accounts.models import User


class UserAnalytics(models.Model):
    profile_visits = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facebook_visits = models.IntegerField(default=0)
    github_visits = models.IntegerField(default=0)
    linkedin_visits = models.IntegerField(default=0)
    twitter_visits = models.IntegerField(default=0)
    medium_visits = models.IntegerField(default=0)
    last_updated = models.DateTimeField(default=now)
    # TODO ADD UNSPLASH VISITS once merged
