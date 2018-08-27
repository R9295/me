from django.urls import path

from .views import MediumFeedView

urlpatterns = [
    path('medium/<str:prefix>', MediumFeedView.as_view(), name='medium'),
]
