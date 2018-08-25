from django.urls import path

from .views import FeedbackView

urlpatterns = [
    path('me/feedback', FeedbackView.as_view(), name='add_feedback'),
]
