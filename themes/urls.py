from django.urls import path

from .views import PreviewThemeView

urlpatterns = [
    path('<str:theme_id>', PreviewThemeView.as_view(), name='preview')
]
