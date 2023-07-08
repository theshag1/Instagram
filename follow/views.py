from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import FollowSerializer


# Create your views here.


class FollowApi(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FollowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('followed_user')
        return Response(serializer.data)