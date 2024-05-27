from rest_framework import serializers

from .models import DotaBlocks


class DotaBlocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = DotaBlocks
        fields = '__all__'