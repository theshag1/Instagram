from rest_framework import serializers
from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = (
            'follow',
            'followed_user'
        )

    read_only_fields = ('id',)



