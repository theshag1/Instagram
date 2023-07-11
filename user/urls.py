from django.urls import path
from user.views import UserApiview, LoginApiView, LogoutApiView, UserUpdateDestoryAPI , UserRegisterApi , UserFollowedAPI , UserFollowersAPI  ,User_Password_change , UserUpdateAPIView

urlpatterns = [
    path('<str:username>/', UserApiview.as_view(), name='user'),
    path('<str:username>/post', UserApiview.as_view(), name='user'),
    path('<str:username>/update/', UserUpdateAPIView.as_view(), name='user'),
    path('<str:username>/followed', UserFollowedAPI.as_view(), name='user-followed'),
    path('<str:username>/followers', UserFollowersAPI.as_view(), name='user-followed'),
    path('register/', UserRegisterApi.as_view(), name='user-register'),
    path('login/', LoginApiView.as_view(), name='user-login'),
    path('logout/', LogoutApiView.as_view(), name='user-logout'),
    path('user/change/password/', User_Password_change.as_view(), name='user'),
]