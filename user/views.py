from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password, make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from follow.models import Follow
from user.models import User
from user.serializer import UserSerilizer, LoginSerializer, LogoutSerializer, UserUpdateView, UserRegisterSerializer, \
    Follows, Password_Update
from django.utils.translation import gettext_lazy as _
from rest_framework import generics


# Create your views here.

class UserApiview(APIView):
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(username=kwargs.get('username'))
        serializer = UserSerilizer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = UserUpdateView(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, requset, *args, **kwargs):
        user = requset.user
        user.delete()
        return Response(f'{user} deleted')


class UserFollowedAPI(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Follow.objects.filter(followed_user=request.user.id)
        serializer = Follows(queryset, many=True)
        return Response(serializer.data)


class UserFollowersAPI(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Follow.objects.filter(follow=request.user.id)
        serializer = Follows(queryset, many=True)
        return Response(serializer.data)


class UserRegisterApi(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class LoginApiView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
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
        else:
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
            return Response()


class UserUpdateAPI(APIView):
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        serializer = UserUpdateView(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = UserUpdateView(instance=self.get_object(pk=self.kwargs.get('pk')), data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = self.get_object(self.kwargs.get('pk'))
        user.delete()
        return Response('user delete')


class UserUpdateDestoryAPI(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateView


class User_Password_change(APIView):
    def post(self, request, *args, **kwargs):
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
            return Response(serializer.data)
        else:
            return Response('error')


"""

    def post(self, request, *args, **kwargs):
        serializer = UserUpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = User.objects.filter(username=username).first()
        password = serializer.validated_data.get('password')
        new_password = serializer.validated_data.get('new_password')
        is_validate = check_password(password, user.password)
        if is_validate:
            user.set_password(new_password)
            user.save()
            return Response(serializer.data)
        else:
            return Response({"error": "Correct username or password"})



"""
