from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAuthenticated
from .models import User, UserCode
from lol.models import UserLol
from lol.serializers import UserCourseSerializer
from .serializers import UserSerializer, RegistrUserSerializer, UserLoginSerializer, EmailSerializer
from django.contrib.auth import authenticate, login
from .utils import send_code
from .procents import lol_procents


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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.values('username', 'email', 'points')
        serializer = UserSerializer(user, many=True)
        user_courses = UserLol.objects.filter(user_id=User.objects.get(pk=request.user.id)).values('course_name').distinct()
        serializer2 = UserCourseSerializer(user_courses, many=True)
        progress = lol_procents(request)
        return Response({'courses': progress,
                        'user': serializer.data})

    def put(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer = UserSerializer(many=True)
        if request.user.email != request.email:
            user.is_verified = 0
            send_code(request.email)
        return Response(serializer.data)



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