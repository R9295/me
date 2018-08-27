from django.urls import path

from .views import MediumFeedView, UnsplashFeedView

urlpatterns = [
    path('medium/<str:prefix>', MediumFeedView.as_view(), name='medium'),
    path('unsplash/<str:prefix>', UnsplashFeedView.as_view(), name='unsplash'),
]
