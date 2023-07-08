from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post
from .serializer import PostSerializer


# Create your views here.

class PostAPi(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(user_id=request.user.id)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
