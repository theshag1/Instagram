from rest_framework import serializers

from post.models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'user',
            'image_or_vidio',
            'about',
            'like',
            'comment'

        )
        read_only_fields = ('id',)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'post',
        )
        read_only_fields = ('id', 'liked_user')
