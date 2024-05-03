from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.forms.models import model_to_dict
from rest_framework import generics
from rest_framework import status
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication


from .permissions import IsAuthenticated
from .models import User, UserCode
from .serializers import UserSerializer, RegistrUserSerializer, UserLoginSerializer, EmailSerializer
from django.contrib.auth import get_user, authenticate, login
from .utils import send_code


class UserAPIRegistr(GenericAPIView):
    serializer_class = RegistrUserSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_code(user['email'])
            return Response({'data': user})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        print(request.data)
        if self.request.user.is_authenticated:
            return Response({'request.data': str(get_user(request=request))}, status=status.HTTP_200_OK)
        return Response({'ok': 'ee'})


class EmailVerify(GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        code = request.data.get('code')
        try:
            user_code = UserCode.objects.get(code=code)
            user = user_code.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({'message': 'OK'}, status=status.HTTP_200_OK)
            return Response({'message': 'code is invalid'})
        except UserCode.DoesNotExist:
            return Response({'message': 'code not provided'})


class LoginUserView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        token = user.tokens()
        login(request, user)
        return Response({
                'username': user.username,
                'access_token': str(token.get('access')),
                'refresh_token': str(token.get('refresh')),
                })