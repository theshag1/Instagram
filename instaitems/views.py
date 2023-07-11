from django.shortcuts import render
from rest_framework import generics

from post.models import Post
from post.serializer import PostSerializer


# Create your views here.


class PostAPIV(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
