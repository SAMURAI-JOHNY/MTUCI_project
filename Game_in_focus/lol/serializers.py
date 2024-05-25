from rest_framework import serializers

from .models import LolBlocks, UserLol
from gameinfocus.models import User


class LolSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLol
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.username = validated_data.username
        instance.email = validated_data.email


class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLol
        fields = ['course_name']


class BlocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = LolBlocks
        fields = '__all__'

