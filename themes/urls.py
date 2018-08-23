from django.urls import path

from .views import PreviewImageView, PreviewThemeView

urlpatterns = [
    path('<str:theme_id>', PreviewThemeView.as_view(), name='preview'),
    path('preview/image', PreviewImageView.as_view(), name='preview_img'),
]
