from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.models import Profile


class PreviewThemeView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PreviewThemeView, self).get_context_data()
        # TODO move this user data to settings.py for a default global Profile
        # and iterate over dict to clean this up
        first_name = self.request.GET.get('first_name') or 'Johnny'
        last_name = self.request.GET.get('last_name') or 'Rotten'
        description = self.request.GET.get('description') or 'I AM TEST'
        short_description = self.request.GET.get('short_description') or 'Developer, Open Source Enthusiast'
        context['user'] = Profile(first_name=first_name, last_name=last_name,
                                  description=description, short_description=short_description)
        return context

    def get_template_names(self):
        # set the theme name to the url param
        return ['themes/{0}.html'.format(self.kwargs.get('theme_id'))]
