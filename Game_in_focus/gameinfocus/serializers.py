from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from .models import User, UserCode
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_str, smart_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'points']
        read_only_fields = ['points']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class UserLoginSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'access_token', 'refresh_token']


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


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCode
        fields = ['user', 'code']


class ResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).existits():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            site_domain = get_current_site(request).domain
            relative_link = reverse('reset ok', kwargs={'uidb64': uidb64, 'token': token})
            abslink = f'http://{site_domain}{relative_link}'
            data = {
                'emal_body': f'Ссылка для сброса пароля {abslink}',
                'email_subject': 'Reset your Password',
                'to_email': user.email
            }

        return super().validate(data)


class NewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True)
    confirm_password = serializers.CharField(max_length=255, write_only=True)
    uidb64 = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']


class LogoutSerializer(serializers.ModelSerializer):
    refresh_token = serializers.CharField()

    class Meta:
        model = User
        fields = ['refresh_token']

    def validate(self, data):
        self.token = data.get('refresh_token')
        return data

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad token')

