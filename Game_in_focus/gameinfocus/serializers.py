from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework.response import Response

from .models import User, UserDota, UserLol, LolBlocks, Lol
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegistrUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get('password', '')
        password2 = data.get('password2', '')
        if password != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]


class LolSerializer(serializers.ModelSerializer):
    class Meta:
        model = LolBlocks
        fields = '__all__'




