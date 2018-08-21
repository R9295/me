from django.core.management.base import BaseCommand
from accounts.models import User
from django.utils.timezone import now


class Command(BaseCommand):
    help = "Sets profiles to inactive if the end date has passed"

    def handle(self, *args, **options):
        for user in User.objects.all():
            if user.end_date < now():
                if user.profile:
                    user.profile.active = False
                    user.profile.save()
                    self.stdout.write(self.style.SUCCESS('Disabling {} cause end_date\
                    exceeds now'.format(user.pk)))
