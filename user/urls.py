from django.urls import path
from user.views import UserAPIView, \
    UserFollowedAPIView, UserFollowersAPIView, User_Password_change, UserPostAPIView, \
    UserPostDetailAPIView, UserPostCommentAPIView, UserPostLikeAPIView, UserUpdateAPI, UsersLastMovementAPI, UserQrCOde, \
    EmailVarification, CheckEmailVarificationCode

urlpatterns = [
    # requirment
    path('qr/', UserQrCOde.as_view(), name='user_qr_code'),
    path('email/varification/', EmailVarification.as_view(), name='user_email_varification_code'),
    path('email/varification/check/', CheckEmailVarificationCode.as_view(), name='user_email_varification_code'),
    path('<str:username>/lastmovament/', UsersLastMovementAPI.as_view(), name='user'),
    path('<str:username>/changepassword/', User_Password_change.as_view(), name='user'),
    path('<str:username>/', UserAPIView.as_view(), name='user'),
    path('<str:username>/post/', UserPostAPIView.as_view(), name='user_post'),
    path('<str:username>/post/<int:pk>/', UserPostDetailAPIView.as_view(), name='user_post'),
    path('<str:username>/post/<int:pk>/comment/', UserPostCommentAPIView.as_view(), name='user_post'),
    path('<str:username>/post/<int:pk>/like/', UserPostLikeAPIView.as_view(), name='user_post'),
    path('<str:username>/update/', UserUpdateAPI.as_view(), name='user'),
    path('<str:username>/followed/', UserFollowedAPIView.as_view(), name='user-followed'),
    path('<str:username>/followers/', UserFollowersAPIView.as_view(), name='user-followed')

]
