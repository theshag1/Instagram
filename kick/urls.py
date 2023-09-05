from django.urls import path

from .views import SpamAPI

urlpatterns = [
    path('', SpamAPI.as_view(), name='spam_api')
]
