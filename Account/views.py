from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password, make_password

from config import settings
from post.models import Post
from post.serializer import PostSerializer
# Create your views here.
from user.models import User, UserStory
from .models import UpdateCode

from user.serializer import LoginSerializer, UserSerilizer, LogoutSerializer, UserRegisterSerializer, Password_change, \
    Check_code, UserForgotPasswordUpdate, Password_Update, UserStorySerializer

from Massages import subject
from Massages import messages
import datetime

from rest_framework.permissions import IsAuthenticated


class BasicUserView(APIView):
    def get(self, request, *args, **kwargs):
        post_queryset = Post.objects.order_by('-id')
        story_queryset = UserStory.objects.all()
        post_serializer = PostSerializer(post_queryset, many=True)
        story_serializer = UserStorySerializer(story_queryset, many=True)
       # yeap
        return Response({"posts": post_serializer.data, "stores": story_serializer.data})


class LoginUser(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = User.objects.filter(username=username).first()
        is_user = check_password(password, user.password)
        email = user.email
        massage = f"Hi dear {request.user.username} , \nWe found out your login to your account  on time{datetime.datetime.now()} , \n if this dont be you change your profile password here : {f'http://127.0.0.1:8000/user/{user.username}/changepassword/'}"
        if is_user:
            login(request, user=user)
            send_mail(subject=subject.EMAIL_LOGIN_SUBJECT, message=massage, from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[email])
            return Response(data={"successful": f"Login successful from user {request.user.username}"})
        return Response(data={'Detail': 'Please input true username or password'})


class LogoutUser(APIView):
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(id=request.user.id)
        serializer = UserSerilizer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ask_validate = serializer.validated_data.get('ask_validate')
        if ask_validate in ['Yes', 'yes']:
            logout(
                request
            )
            return Response(data={"detail": f"You successful exit user {request.user.username}"})


class UserRegisterApi(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class SendCodeForUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Password_change(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_user = User.objects.filter(username=serializer.validated_data.get('username')).first()
        if is_user:
            code_varification = get_random_string(allowed_chars='123456789', length=6)
            update_code = (
                UpdateCode.objects.create(
                    email=is_user.email,
                    data_sent=datetime.datetime.now(),
                    code=code_varification,
                    is_check=False
                )
            )
            update_code.save()
            send_mail(
                subject=subject.Forget_password,
                message=messages.forgot_password(username=is_user, code=code_varification),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[is_user.email]
            )
            return Response(status=status.HTTP_302_FOUND,
                            headers={"Location": "http://127.0.0.1:8000/profile/checksendcode/"})
        else:
            return Response(data={"error": "Can't found this user"})


class CheckCodeSendAPIView(generics.CreateAPIView):
    queryset = UpdateCode.objects.all()
    serializer_class = Check_code

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        code = serializer.validated_data.get("code")
        user = User.objects.filter(email=email).first()
        update_code = self.get_queryset().filter(email=email, code=code, is_check=False).order_by('-data_sent').first()
        if update_code and update_code.code != code:
            raise ValidationError('Update code  invalid')

        update_code.is_check = True
        update_code.save(update_fields=["is_check"])
        login(
            request, user=user
        )
        return Response(status=status.HTTP_302_FOUND, headers={
            "Location": "http://127.0.0.1:8000/profile/whaenuserdasiu32kiogbwqyfiwdfwuiefhwiuefhwodasoiewhfuvu23/"})


class Step4ForUpdatePasscode(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserForgotPasswordUpdate(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password1 = serializer.validated_data.get('new_password1')
        new_password2 = serializer.validated_data.get('new_password2')
        if new_password1 != new_password2:
            raise ValidationError('Not allowed password is incorrect')
        user = User.objects.filter(id=request.user.id)

        user.update(password=make_password(new_password1))
        if user:
            return Response(data={"detail": "Successful changed user"})
        return Response('error')


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
