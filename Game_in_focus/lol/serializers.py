from rest_framework import serializers

from .models import LolBlocks


class LolSerializer(serializers.ModelSerializer):
    class Meta:
        model = LolBlocks
        fields = '__all__'