from rest_framework import serializers

from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'user',
            'image_or_vidio',
            'like',
            'comment'

        )
        read_only_fields = ('id',)
