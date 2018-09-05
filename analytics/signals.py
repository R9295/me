from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Profile

from .models import ProfileAnalytics


@receiver(post_save, sender=Profile)
def create_analytics_profile(sender, instance, created, **kwargs):
    if created:
        ProfileAnalytics.objects.create(profile=instance)
