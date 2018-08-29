from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from analytics.models import UserAnalytics


class Command(BaseCommand):
    help = "Clears analytics of users if they're more than a month old"

    def handle(self, *args, **options):
        for user in UserAnalytics.objects.all():
            if user.last_updated > now() - relativedelta(days=32):
                user.profile_visits = 0
                user.medium_visits = 0
                user.facebook_visits = 0
                user.twitter_visits = 0
                user.github_visits = 0
                user.linkedin_visits = 0
                user.last_updated = now()
                user.save()
