import glob

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase


class TestThemes(TestCase):
    def test_delete_preview_images_command(self):
        with open(settings.BASE_DIR+'/media/previews/test', 'wb+') as destination:
            destination.write(b'asd')
        call_command('delete_preview_images')
        files = glob.glob(settings.BASE_DIR+'/media/previews/*')
        self.assertEqual(files, [])
