from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.forms.models import model_to_dict
from rest_framework import generics
from rest_framework import status

from .models import User, UserDota, UserLol, Lol, LolBlocks
from .serializers import UserSerializer, RegistrUserSerializer, LolSerializer
from django.contrib.auth import get_user_model


class UserAPIRegistr(GenericAPIView):
    serializer_class = RegistrUserSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user=serializer.data
            return Response({'data': user})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPILol(GenericAPIView):
    serializer_class = LolSerializer

    def get(self, request, *args, **kwargs):
        block_id = kwargs.get('block_id')
        user_inf = LolBlocks.objects.get(pk=block_id)
        serializer = LolSerializer(user_inf)
        return Response({'data': serializer.data})






class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#user_inf = User.objects.get(pk=request.user.id)
#serializer = UserSerializer(user_inf)

