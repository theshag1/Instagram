from django.urls import path
from .views import LoginUser, UserRegisterApi, LogoutUser

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login-user'),
    path('logout/', LogoutUser.as_view(), name='login-user'),
    path('register/', UserRegisterApi.as_view(), name='user-register'),


]
