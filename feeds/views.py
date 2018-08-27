from django.views.generic import View
from django.http import JsonResponse
import requests
import json
from core.models import Profile
from django.shortcuts import get_object_or_404


class MediumFeedView(View):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, prefix=kwargs.get('prefix'), feed="medium")
        medium_username = profile.medium[profile.medium.index('.com/')+5:]
        r = requests.get(
        'https://medium.com/{0}?format=json'.format(medium_username)
        )
        _json = json.loads(r.text[r.text.find('{'):])
        posts = []
        for k,v in _json['payload']['references']['Post'].items():
            posts.append({
                'url': 'https://medium.com/{0}/{1}'.format(medium_username, k),
                'title': v['title'],
                'preview': v['previewContent']['subtitle'],
                })
        return JsonResponse({
        'response': 'success',
        'data': posts,
        })
