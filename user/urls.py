from django.urls import path
from user.views import (
    UserAPIView,
    UserFollowedAPIView, UserFollowersAPIView, UserPostAPIView,
    UserPostDetailAPIView, UserPostCommentAPIView, UserPostLikeAPIView, UserUpdateAPI,
    UsersLastMovementAPI, UserQrCOde,
    EmailVarification, CheckEmailVarificationCode,
    UserStoryAPIview,
    UserStoryCreatedAPI, UserStorySavedAPIview, UserStorySavedDetailAPIview, SavedPostAPIView, SavedPostDetail)

urlpatterns = [
    # requirment

    path('<str:id>/saved/', SavedPostAPIView.as_view(), name='saved_post'),
    path('<str:id>/saved/<int:pk>', SavedPostDetail.as_view(), name='saved_post_pk'),

    path('<str:username>/archived/story/<int:pk>', UserStorySavedDetailAPIview.as_view(),
         name='user_crreate_archived'),
    path('<str:username>/archived/story', UserStorySavedAPIview.as_view(), name='user_crreate_archived'),
    path('<str:username>/story/create', UserStoryCreatedAPI.as_view(), name='user_crreate_story'),
    path('<str:username>/story', UserStoryAPIview.as_view(), name='saved_post'),
    path('qr/', UserQrCOde.as_view(), name='user_qr_code'),
    path('email/varification/', EmailVarification.as_view(), name='user_email_varification_code'),
    path('email/varification/check/', CheckEmailVarificationCode.as_view(), name='user_email_varification_code'),
    path('<str:username>/lastmovament/', UsersLastMovementAPI.as_view(), name='user'),
    path('<str:username>/', UserAPIView.as_view(), name='user'),
    path('<str:username>/post/', UserPostAPIView.as_view(), name='user_post'),
    path('<str:username>/post/<int:pk>/', UserPostDetailAPIView.as_view(), name='user_post'),
    path('<str:username>/post/<int:pk>/comment/', UserPostCommentAPIView.as_view(), name='user_post'),
    path('<str:username>/post/<int:pk>/like/', UserPostLikeAPIView.as_view(), name='user_post'),
    path('<str:username>/update/', UserUpdateAPI.as_view(), name='user'),
    path('<str:username>/followed/', UserFollowedAPIView.as_view(), name='user-followed'),
    path('<str:username>/followers/', UserFollowersAPIView.as_view(), name='user-followed'),
]
