from django.urls import path
from .views import PostAPi, LikeAPI

urlpatterns = [
    path('', PostAPi.as_view(), name='post_user'),
    path('like/', LikeAPI.as_view(), name='post_like')
]
