from django.urls import path
from .views import PostAPi, LikeAPI, PostDetail, ArchivedPostAPIVew

urlpatterns = [
    path('archived/', ArchivedPostAPIVew.as_view(), name='archived-post'),
    path('', PostAPi.as_view(), name='post'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('like/', LikeAPI.as_view(), name='post_like')
]
