from rest_framework import serializers
from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = (
            'follow',
        )

    read_only_fields = ('id', 'followed_user')



"""
{
        "follow":3,
        "followed_user":1
}

"""
