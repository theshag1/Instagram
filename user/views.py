import datetime
import os
from random import random

import qrcode
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.http import Http404
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

import user.models
from config import settings
from follow.models import Follow
from user.models import User
from user.serializer import UserSerilizer, LoginSerializer, LogoutSerializer, UserUpdateView, UserRegisterSerializer, \
    Follows, Password_Update, EmailVarificationCode, SendEmailVarification
from post.models import Post, Comment, Like
from post.serializer import PostSerializer, CommentSerializer, LikeSerializer
from items.url import url
from Massages import (subject, messages)
from .models import VarificationCode

""" 
             user site api view
#########################################################################################
"""


# class BasicAPI(APIView):
#     def get(self, request, *args, **kwargs):
#
#

class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(username=kwargs.get('username'))
        serializer = UserSerilizer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFollowedAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Follow.objects.filter(followed_user__username=kwargs.get('username'))
        serializer = Follows(queryset, many=True)
        is_user = User.objects.filter(username=kwargs.get('username'))
        if is_user:
            return Response(serializer.data)
        return Response(data={"error": f"{kwargs.get('username')} not found"})


class UserFollowersAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Follow.objects.filter(follow__username=kwargs.get('username'))
        serializer = Follows(queryset, many=True)
        is_user = User.objects.filter(username=kwargs.get('username'))
        if is_user:
            return Response(serializer.data)
        return Response(data={"error": f"{kwargs.get('username')} not found"})


class UserPostAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(user__username=kwargs.get('username'))
        serializer = PostSerializer(queryset, many=True)
        is_user = User.objects.filter(username=kwargs.get('username'))
        if is_user:
            if queryset:
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(data={"detail": f"{kwargs.get('username')} haven't post"})

        return Response(data={"error": f"{kwargs.get('username')} not found"})


class UserPostDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(id=kwargs.get('pk'))
        serializer = PostSerializer(queryset, many=True)
        is_user = User.objects.filter(
            username=kwargs.get('username')
        )
        if is_user:
            if queryset:
                return Response(serializer.data)
            return Response(data={"error": f"{kwargs.get('username')} haven't {kwargs.get('pk')} th post"})
        return Response(data={"error": f"{kwargs.get('username')} can't find"})


class UserPostCommentAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(post_id=kwargs.get('pk'))
        serializer = CommentSerializer(queryset, many=True)
        is_user = User.objects.filter(
            username=kwargs.get('username')
        )
        if is_user:
            if queryset:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(data={"detail": "haven't comment yet "})
        return Response(data={"error": f"{kwargs.get('username')} can't find"})


class UserPostLikeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Like.objects.filter(post_id=kwargs.get('pk'))
        serializer = LikeSerializer(queryset, many=True)
        is_user = User.objects.filter(
            username=kwargs.get('username')
        )
        if is_user:
            if queryset:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(data={"detail": "cannot find"})
        return Response(data={"error": f"{kwargs.get('username')} can't find"})


class UsersLastMovementAPI(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Follow.objects.filter(follow__username=kwargs.get('username'))
        queryset2 = Post.objects.filter(user_id=request.user.id)
        serializer = UserSerilizer(queryset, many=True)
        serializer2 = PostSerializer(queryset2, many=True)
        return Response({"user": serializer.data, "post": serializer2.data})


class UserQrCOde(APIView):
    def get(self, request, *args, **kwargs):
        data_to_scand = f"User : {request.user.username} , User photo {request.user.profile_photo}"
        qr_code_file = f"{request.user.username}_qr_code.png"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_to_scand)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_code_file)

        return Response({"Detail": f"Qr code here {qr_code_file}"})

    """
                       user requirement 
    #########################################################################################
    """

    class UserRegisterApi(generics.CreateAPIView):
        queryset = User.objects.all()
        serializer_class = UserRegisterSerializer


class EmailVarification(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendEmailVarification(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('email')
        code = get_random_string(allowed_chars='1234567890', length=6)
        is_user = User.objects.filter(email=user).first()
        if is_user:
            code = (VarificationCode.objects.create(email=is_user.email, is_varification=False, code=code,
                                                    date=datetime.datetime.now()))
            send_mail(
                subject=subject.EMAIL_LOGIN_SUBJECT, message=messages.email_varification(is_user.username, code),
                from_email=settings.EMAIL_HOST_USER, recipient_list=[is_user.email]

            )
            return Response(serializer.data)
#
#
# class CheckEmailVarificationCode(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = EmailVarificationCode(data=request.data)
#         serializer.is_valid(raise_exception=True)
#

""""
    class LoginApiView(APIView):
        def post(self, request, *args, **kwargs):
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = User.objects.filter(username=username).first()
            validate = check_password(password, user.password)
            if validate:
                login(
                    request, user=user
                )
                return Response(serializer.data)

        
            return Response(data={"error": "Password or Username correct"})
            
         class LogoutApiView(APIView):
        @swagger_auto_schema(request_body=LogoutSerializer)
        def post(self, request, *args, **kwargs):
            serializer = LogoutSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = request.user
            ask = serializer.validated_data.get('ask_validate')
            if ask == 'Yes':
                logout(
                    request
                )
                return Response(data=_(f'Logout from user {user}'))
            else:
                return Response(status=status.HTTP_100_CONTINUE)
                """


class UserUpdateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(username=kwargs.get('username'))
        if kwargs.get('username') == request.user.username:
            serializer = UserSerilizer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data={'error': 'Object not found'})

    def put(self, request, *args, **kwargs):
        serializer = UserUpdateView(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        if kwargs.get('username') == request.user.username:
            user = request.user
            user.delete()
            return Response(f'{user} deleted')
        return Response(data={'error': 'Object not found'})


class UserUpdateAPI(APIView):
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, *args, **kwargs):
        if kwargs.get('username') == request.user.username:
            pk = kwargs.get('pk')
            serializer = UserUpdateView(self.get_object(pk))
            return Response(serializer.data)
        return Response(data={"error": "You can't update another users"})

    def put(self, request, *args, **kwargs):
        if kwargs.get('username') == request.user.username:

            serializer = UserUpdateView(instance=self.get_object(pk=self.kwargs.get('pk')), data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"error": f"You cannot update user : {kwargs.get('username')}"})

    def delete(self, request, *args, **kwargs):
        user = self.get_object(self.kwargs.get('pk'))
        user.delete()
        return Response(data={'detail': f'{user} deleted'})


class UserUpdateDestoryAPI(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateView


class User_Password_change(APIView):
    @swagger_auto_schema(request_body=Password_Update)
    def post(self, request, *args, **kwargs):
        if kwargs.get('username') == request.user.username:
            serializer = Password_Update(data=request.data)
            serializer.is_valid(raise_exception=True)
            username = serializer.validated_data.get('username')
            user = User.objects.filter(username=username).first()
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
            validate = check_password(old_password, user.password)

            if validate:
                user.set_password(new_password)
                user.save()
                send_mail(
                    subject=subject.CHANGE_PASSWORD_WARNING,
                    message=messages.change_message(user.username, datetime.datetime.now()),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email]
                )
                return Response(serializer.data)
            else:
                return Response('error')
        return Response(data={'error': f"You can't change password {kwargs.get('username')}"})
