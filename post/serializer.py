from rest_framework import serializers

from post.models import Post, Like, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'image_or_vidio',
            'like',
            'comment',

        )
        read_only_fields = ('user',)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'post',
            'liked_user'
        )
        read_only_fields = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'post',
            'body',
            'comment_like'
        )


class PostArchive(serializers.Serializer):
    post = serializers.IntegerField()
