from django.urls import path
from user.views import UserApiview, LoginApiView, LogoutApiView, UserUpdateDestoryAPI , UserRegisterApi

urlpatterns = [
    path('profile/', UserApiview.as_view(), name='user'),
    path('register/', UserRegisterApi.as_view(), name='user-register'),
    path('login/', LoginApiView.as_view(), name='user-login'),
    path('logout/', LogoutApiView.as_view(), name='user-logout'),
    path('<int:pk>/update/', UserUpdateDestoryAPI.as_view(), name='user-update'),
]
