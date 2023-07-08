from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.serializer import UserSerilizer, LoginSerializer, LogoutSerializer, UserUpdateView, UserRegisterSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import generics


# Create your views here.

class UserApiview(APIView):
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(id=request.user.id)
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


class UserRegisterApi(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


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
        else:
            return Response(data={"error": "Password or Username correct"})


class LogoutApiView(APIView):
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
