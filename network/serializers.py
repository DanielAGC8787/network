from .models import *
from rest_framework import serializers

class UserSerialzer(serializers.ModelSerializer):
    followers = serializers.StringRelatedField(many=True)
    followings = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'followers', 'followings']
