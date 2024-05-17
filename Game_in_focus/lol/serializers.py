from rest_framework import serializers

from .models import LolBlocks, UserLol
from gameinfocus.models import User


class LolSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLol
        fields = '__all__'

    def create(self, validated_data):
        return UserLol.objects.create(**validated_data)


class BlocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = LolBlocks
        fields = '__all__'

