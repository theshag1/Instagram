import email

from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password

from config import settings
# Create your views here.
from user.models import User
from .models import UpdateCode

from user.serializer import LoginSerializer, UserSerilizer, LogoutSerializer, UserRegisterSerializer, Password_change
from Massages import subject
from Massages import messages
import datetime


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


# subject = 'Verification code'
#       email_user_name = email.split('@')[0]
#       massage = f'Hi {email_user_name} 👋🏻, your email verifcation code is :{code}'
#       send_mail(subject, massage, from_email=settings.EMAIL_HOST_USER, recipient_list=[email])

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
                    user_id=request.user.id,
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
            return Response(data={"detail": f"Successful send email {is_user.email}"})
        else:
            return Response(data={"error": "Can't found this user"})
