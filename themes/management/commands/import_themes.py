from django.core.management.base import BaseCommand

from themes.models import Theme
from themes.themes import THEME_LIST


class Command(BaseCommand):
    help = "Imports all themes if they don't exist, used for adding new themes."

    def handle(self, *args, **options):
        for theme in THEME_LIST:
            if Theme.objects.filter(pk=theme['uuid']).count() != 1:
                # if not one, import theme
                Theme.objects.create(id=theme['uuid'], name=theme['name'])
                self.stdout.write(self.style.SUCCESS('Successfully imported theme \
                {}'.format(theme['name'])))
            else:
                self.stdout.write(self.style.SUCCESS('ignoring theme {} \
                 as it already exists'.format(theme['name'])))
