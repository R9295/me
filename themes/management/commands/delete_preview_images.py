import glob
import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Deletes all preview images in the folder"

    def handle(self, *args, **options):
        files = glob.glob(settings.BASE_DIR+'/media/previews/*')
        for f in files:
            os.remove(f)
            self.stdout.write(self.style.SUCCESS('deleted {}'.format(f)))
