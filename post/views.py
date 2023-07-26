from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post, Like, Comment
from user.models import User
from .serializer import PostSerializer, LikeSerializer, CommentSerializer, PostArchive


# Create your views here.

class PostAPi(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(user_id=request.user.id, is_archived=False)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class LikeAPI(APIView):
    @swagger_auto_schema(request_body=LikeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post_id = serializer.validated_data.get('post')
        is_object = Like.objects.filter(post_id=post_id)
        if post_id and is_object:
            is_object.delete()
            return Response(data={'detail': 'Unliked'})
        else:
            Like.objects.create(liked_user=request.user, post=post_id)
            return Response(data={'detail': 'Liked'})


class PostDetail(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(id=kwargs.get('pk'), is_archived=False)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PostArchive(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_post = Post.objects.get(id=serializer.validated_data.get('post'))
        if is_post:
            Post.objects.filter(id=serializer.validated_data.get('post')).update(is_archived=True)
            return Response(data={'detail': 'Succesfuly add Archived'})
        return Response(data={"error": "error ! "})


class ArchivedPostAPIVew(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(user_id=request.user.id, is_archived=True)
        serializer = PostSerializer(
            queryset, many=True
        )
        return Response(serializer.data)
