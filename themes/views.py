import uuid

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

DEFAULT_USER = {
    'first_name': 'Joe',
    'last_name': 'Strummer',
    'description': '# TEST',
    'short_description': 'The Clash',
    'github': None,
    'facebook': None,
    'linkedin': None,
    'medium': None,
    'twitter': None,
    'image': None,
}


def handle_uploaded_file(f, name):
    with open(settings.BASE_DIR+'/media/previews/'+name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class PreviewImageView(View):
    def post(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        if image is not None and 'image' in image.content_type:
            name = str(uuid.uuid4()) + image.name[image.name.find('.'):]
            handle_uploaded_file(image, name)
            return JsonResponse({'url': '/media/previews/'+name})
        else:
            return JsonResponse({'error': 'failed'})


class PreviewThemeView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PreviewThemeView, self).get_context_data()
        user = DEFAULT_USER
        for k, v in user.items():
            if self.request.GET.get(k):
                if k == 'image':
                    if self.request.GET.get(k) == 'none':
                        user[k] = self.request.user.profile.image
                    elif self.request.GET.get(k) == 'clear':
                        user[k] = None
                    else:
                        user[k] = {'url': self.request.GET.get(k)}
                else:
                    user[k] = self.request.GET.get(k)

        context['user'] = user
        return context

    def get_template_names(self):
        # set the theme name to the url param
        return ['themes/{0}.html'.format(self.kwargs.get('theme_id'))]
