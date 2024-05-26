from rest_framework import serializers

from .models import LolBlocks, UserLol
from gameinfocus.models import User


class LolSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLol
        fields = '__all__'


class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLol
        fields = ['course_name']


class BlocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = LolBlocks
        fields = '__all__'

