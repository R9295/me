from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from analytics.models import ProfileAnalytics


class Command(BaseCommand):
    help = "Clears analytics of profiles if they're more than a month old"

    def handle(self, *args, **options):
        for profile in ProfileAnalytics.objects.all():
            if profile.last_updated > now() - relativedelta(days=32):
                profile.profile_visits = 0
                profile.medium_visits = 0
                profile.facebook_visits = 0
                profile.twitter_visits = 0
                profile.github_visits = 0
                profile.linkedin_visits = 0
                profile.last_updated = now()
                profile.save()
