from django.urls import path
from .views import PostAPi

urlpatterns = [
    path('', PostAPi.as_view(), name='post_user')
]
