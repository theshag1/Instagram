from django.urls import path
from .views import FollowApi

urlpatterns = [
    path('', FollowApi.as_view(),name='follow')
]
