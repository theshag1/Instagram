from django.contrib.auth import login
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from follow.models import Follow
from user.models import User
from user.serializer import UserSerilizer, LoginSerializer


# Create your views here.

class UserApiview(APIView):
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(id=request.user.id)
        serializer = UserSerilizer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        user = User.objects.filter(username=username).first()
        validate = User.objects.filter(password=password)
        if validate:
            login(
                request, user=user
            )
            return Response(serializer.data)
        else:
            return Response(data={"error": "Password or Username correct"})
