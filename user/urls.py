from django.urls import path
from user.views import UserAPIView, LoginApiView, LogoutApiView, UserRegisterApi, \
    UserFollowedAPIView, UserFollowersAPIView, User_Password_change, UserUpdateAPIView, UserPostAPIView, \
    UserPostDetailAPIView ,UserPostCommentAPIView ,UserPostLikeAPIView ,UserUpdateAPI
urlpatterns = [
    # site
    path('<str:username>/', UserAPIView.as_view(), name='user'),
    path('<str:username>/post', UserPostAPIView.as_view(), name='user_post'),
    path('<str:username>/post/<int:pk>/', UserPostDetailAPIView.as_view(), name='user_post'),
    path('<str:username>/post/<int:pk>/comment/', UserPostCommentAPIView.as_view(), name='user_post'),
    path('<str:username>/post/<int:pk>/like/', UserPostLikeAPIView.as_view(), name='user_post'),
    path('<str:username>/update/', UserUpdateAPI.as_view(), name='user'),
    path('<str:username>/followed/', UserFollowedAPIView.as_view(), name='user-followed'),
    path('<str:username>/followers/', UserFollowersAPIView.as_view(), name='user-followed'),
    # requirment
    path('register/', UserRegisterApi.as_view(), name='user-register'),
    path('login/', LoginApiView.as_view(), name='user-login'),
    path('logout/', LogoutApiView.as_view(), name='user-logout'),
    path('user/changepassword/', User_Password_change.as_view(), name='user'),
]
