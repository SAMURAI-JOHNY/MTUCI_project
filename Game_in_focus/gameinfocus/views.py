from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAuthenticated
from .models import User, UserCode
from lol.models import UserLol
from lol.serializers import UserCourseSerializer
from .serializers import UserSerializer, RegistrUserSerializer, UserLoginSerializer, EmailSerializer, ResetSerializer
from .serializers import NewPasswordSerializer, LogoutSerializer
from django.contrib.auth import authenticate, login
from .utils import send_code
from .procents import lol_procents
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserAPIRegistr(GenericAPIView):
    def post(self, request):
        user_data = request.data
        serializer = RegistrUserSerializer(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_code(user['email'])
            return Response({'data': user})
        print(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer = UserSerializer(user)
        user_courses = UserLol.objects.filter(user_id=User.objects.get(pk=request.user.id)).values('course_name').distinct()
        serializer2 = UserCourseSerializer(user_courses, many=True)
        progress = lol_procents(request)
        return Response({'courses': progress,
                        'user': serializer.data
                         }, status=status.HTTP_200_OK)

    def patch(self, request):
        user = User.objects.get(pk=request.user.id)
        print(request.data)
        serializer = UserSerializer(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if request.user.email != request.data.get('email'):
            user.is_verified = 0
            send_code(request.data.get('email'))
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        return Response({
                'username': user.username,
                'access_token': str(token.get('access')),
                'refresh_token': str(token.get('refresh')),
                })


class ResetPasswordView(GenericAPIView):
    def post(self, request):
        serializer = ResetSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'a link in your email'})


class PasswordConfirm(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'succes': True,
                             'message': 'data is valid',
                             'uidb64': uidb64,
                             'token': token
                             }, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({'message': 'invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPassword(GenericAPIView):
    def patch(self, request):
        serializer = NewPasswordSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'password reset sucssesful'}, status=status.HTTP_200_OK)


class LogoutUser(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)