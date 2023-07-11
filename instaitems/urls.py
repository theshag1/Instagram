from django.urls import path
from .views import PostAPIV

urlpatterns = [
    path('', PostAPIV.as_view(), name='post_api')
]
