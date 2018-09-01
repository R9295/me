from django.views.generic import View
from django.http import JsonResponse
import requests
import json
from core.models import Profile
from django.shortcuts import get_object_or_404
from django.conf import settings

class MediumFeedView(View):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, prefix=kwargs.get('prefix'))
        if profile.medium:
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

class UnsplashFeedView(View):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, prefix=kwargs.get('prefix'))
        if profile.unsplash:
            unsplash_username = profile.unsplash[profile.unsplash.index('@')+1:]
            r = requests.get(
                'https://api.unsplash.com/users/{0}/photos?order_by=latest&client_id={1}'.format(
                                                                             unsplash_username,
                                                                             settings.UNSPLASH_ACCESS)
                                                                             )
            images = []
            for i in r.json()[:3]:
                images.append(i['urls']['small'])
            return JsonResponse({
            'response': 'success',
            'data': images,
            })
