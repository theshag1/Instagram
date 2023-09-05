import datetime

import qrcode

from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from UserSavedData.models import UserStoryArchived, SavedPost
from UserSavedData.serializer import UserSavedStorySerializer, UserSavedPostSerializer
from config import settings
from follow.models import Follow
from user.models import User, VarificationCode, UserStory
from user.serializer import UserSerilizer, UserUpdateView, UserRegisterSerializer, \
    Follows, EmailVarificationCode, SendEmailVarification, UserStorySerializer
from post.models import Post, Comment, Like
from post.serializer import PostSerializer, CommentSerializer, LikeSerializer

from Massages import (subject, messages)

""" 
             user site api view
#########################################################################################
"""


class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_queryset = User.objects.filter(username=kwargs.get('username'))
        post_queryset = Post.objects.filter(user__username=kwargs.get('username'))
        user_serializer = UserSerilizer(user_queryset, many=True)
        post_serializer  = PostSerializer(post_queryset , many=True)
        return  Response(
            {"user_data":user_serializer.data , "post_data" : post_serializer.data}
        )

class UserFollowedAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Follow.objects.filter(followed_user__username=kwargs.get('username'))
        serializer = Follows(queryset, many=True)
        is_user = User.objects.filter(username=kwargs.get('username'))
        if is_user:
            return Response(serializer.data)
        return Response(data={"error": f"{kwargs.get('username')} not found"})


class UserFollowersAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Follow.objects.filter(follow__username=kwargs.get('username'))
        serializer = Follows(queryset, many=True)
        is_user = User.objects.filter(username=kwargs.get('username'))
        if is_user:
            return Response(serializer.data)
        return Response(data={"error": f"{kwargs.get('username')} not found"})


class UserPostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(user__username=kwargs.get('username'), is_archived=False)
        serializer = PostSerializer(queryset, many=True)
        is_user = User.objects.filter(username=kwargs.get('username'))
        if is_user:
            if queryset:
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(data={"detail": f"{kwargs.get('username')} haven't post"})

        return Response(data={"error": f"{kwargs.get('username')} not found"})


class UserPostDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(id=kwargs.get('pk'))
        serializer = PostSerializer(queryset, many=True)
        is_user = User.objects.filter(
            username=kwargs.get('username')
        )
        if is_user:
            if queryset:
                return Response(serializer.data)
            return Response(data={"error": f"{kwargs.get('username')} haven't {kwargs.get('pk')} th post"})
        return Response(data={"error": f"{kwargs.get('username')} can't find"})


class UserPostCommentAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(post_id=kwargs.get('pk'))
        serializer = CommentSerializer(queryset, many=True)
        is_user = User.objects.filter(
            username=kwargs.get('username')
        )
        if is_user:
            if queryset:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(data={"detail": "haven't comment yet "})
        return Response(data={"error": f"{kwargs.get('username')} can't find"})


class UserPostLikeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Like.objects.filter(post_id=kwargs.get('pk'))
        serializer = LikeSerializer(queryset, many=True)
        is_user = User.objects.filter(
            username=kwargs.get('username')
        )
        if is_user:
            if queryset:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(data={"detail": "cannot find"})
        return Response(data={"error": f"{kwargs.get('username')} can't find"})


class UsersLastMovementAPI(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Follow.objects.filter(follow__username=kwargs.get('username'))
        queryset2 = Post.objects.filter(user_id=request.user.id)
        queryset3 = Like.objects.filter(post__user__user=request.user)
        serializer = UserSerilizer(queryset, many=True)
        serializer2 = PostSerializer(queryset2, many=True)
        serilzer3 = LikeSerializer(queryset3, many=True)
        return Response({"user": serializer.data, "post": serializer2.data, "like": serilzer3.data})


class UserQrCOde(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data_to_scand = f"User : {request.user.username} , User photo {request.user.profile_photo}"
        qr_code_file = f"{request.user.username}_qr_code.png"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_to_scand)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_code_file)

        return Response({"Detail": f"Qr code here {qr_code_file}"})


class UserStoryAPIview(APIView):

    def get(self, request, *args, **kwargs):
        queryset = UserStory.objects.filter(user__username=kwargs.get('username'))
        serializer_class = UserStorySerializer(queryset, many=True)
        return Response(serializer_class.data)


class UserStoryCreatedAPI(generics.CreateAPIView):
    queryset = UserStory.objects.all()
    serializer_class = UserStorySerializer

    def create(self, request, *args, **kwargs):
        serilzier = self.get_serializer(data=request.data)
        serilzier.is_valid(raise_exception=True)
        user = serilzier.validated_data.get('user')
        image = serilzier.validated_data.get('image')
        video = serilzier.validated_data.get('video')
        is_user = User.objects.filter(id=request.user.id)
        if is_user:
            UserStoryArchived.objects.create(
                user=user,
                image=image,
                video=video,
                create_data=datetime.datetime.now()
            )
            return Response(data={"detail": "Successfuly created! "})
        return Response(data={"error": 'User not found '})


class UserStorySavedAPIview(APIView):
    def get(self, request, *args, **kwargs):
        if kwargs.get('username') != request.user.username:
            return Response(data={"error": "User erorr !"})
        queryset = UserStoryArchived.objects.filter(user__username=kwargs.get('username'))
        serilizer = UserSavedStorySerializer(queryset, many=True)
        return Response(serilizer.data, status=status.HTTP_200_OK)


class UserStorySavedDetailAPIview(APIView):
    def get_object(self, pk):
        return get_object_or_404(UserStoryArchived, pk=pk)
    def get(self, request, *args, **kwargs):
        serilizer = UserSavedStorySerializer(self.get_object(kwargs.get('pk')))
        if serilizer.data:
            return Response(serilizer.data)
        return Response(data={"error": status.HTTP_204_NO_CONTENT})
    def delete(self, request, *args, **kwargs):
        archived_post = self.get_object(kwargs.get('pk'))
        if archived_post:
            archived_post.delete()
            return Response(status=status.HTTP_302_FOUND,
                            headers={"Location": "http://127.0.0.1:8000/user/shagi/archived/story"})

        return Response(data={"error": status.HTTP_204_NO_CONTENT})
class SavedPostAPIView(APIView):
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            queryset = SavedPost.objects.filter(user=user)
            if queryset.exists():
                serializer = UserSavedPostSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "No saved posts for this user."}, status=200)
        else:
            return Response({"error": "User not found"}, status=404)


class SavedPostDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(SavedPost.objects.filter(pk=pk))

    def get(self, request, *args, **kwargs):
        serializer = UserSavedPostSerializer(self.get_object(kwargs.get('pk')))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_object(kwargs.get('pk'))
        queryset.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


"""
                       user requirement 
    #########################################################################################
"""


class UserRegisterApi(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class EmailVarification(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SendEmailVarification(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        code = get_random_string(allowed_chars='1234567890', length=6)
        is_user = User.objects.filter(username=request.user.username).first()
        if is_user:
            create_code = (VarificationCode.objects.create(email=is_user.email, is_varification=False, code=code,
                                                           date=datetime.datetime.now()))
            User.objects.update(email=email)
            send_mail(
                subject=subject.EMAIL_LOGIN_SUBJECT, message=messages.email_varification(is_user.username, code),
                from_email=settings.EMAIL_HOST_USER, recipient_list=[email]

            )
            return Response(status=status.HTTP_302_FOUND,
                            headers={"Location": "http://127.0.0.1:8000/user/email/varification/check/"})


class CheckEmailVarificationCode(generics.CreateAPIView):
    queryset = VarificationCode.objects.all()
    serializer_class = EmailVarificationCode

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        code = serializer.validated_data.get('code')
        varification = self.get_queryset().filter(email=email, code=code, is_varification=False).order_by(
            '-date').first()
        user = User.objects.filter(username=request.user.username)
        if varification and varification.code == code:
            user.email = email
            varification.is_varification = True
            return Response(data={"detail": "Succesfully Varification ! "})
        else:
            return Response(data={"error": "Can not update ! "})


class UserUpdateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(username=kwargs.get('username'))
        if kwargs.get('username') == request.user.username:
            serializer = UserSerilizer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data={'error': 'Object not found'})

    def put(self, request, *args, **kwargs):
        serializer = UserUpdateView(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        if kwargs.get('username') == request.user.username:
            user = request.user
            user.delete()
            return Response(f'{user} deleted')
        return Response(data={'error': 'Object not found'})


class UserUpdateAPI(APIView):
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, *args, **kwargs):
        if kwargs.get('username') == request.user.username:
            pk = kwargs.get('pk')
            serializer = UserUpdateView(self.get_object(pk))
            return Response(serializer.data)
        return Response(data={"error": "You can't update another users"})

    def put(self, request, *args, **kwargs):
        if kwargs.get('username') == request.user.username:

            serializer = UserUpdateView(instance=self.get_object(pk=self.kwargs.get('pk')), data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"error": f"You cannot update user : {kwargs.get('username')}"})

    def delete(self, request, *args, **kwargs):
        user = self.get_object(self.kwargs.get('pk'))
        user.delete()
        return Response(data={'detail': f'{user} deleted'})


class UserUpdateDestoryAPI(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateView
