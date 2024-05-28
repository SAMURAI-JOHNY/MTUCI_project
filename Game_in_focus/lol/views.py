from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from gameinfocus.models import User
from .models import LolBlocks
from .serializers import BlocksSerializer
from .models import UserLol
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class UserAPILol(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        block_id = kwargs.get('block_id')
        user = User.objects.get(pk=request.user.id)
        lol_inf = LolBlocks.objects.get(pk=block_id)
        user_lol_inf = UserLol.objects.filter(block_id=block_id, user_id=request.user)
        if len(user_lol_inf) == 0:
            user_lol = UserLol(user_id=user, block_id=lol_inf, status=1, block_name=lol_inf.block_name,
                               course_name=lol_inf.course_name)
            user.points += 15
            user.save()
            user_lol.save()
        serializer = BlocksSerializer(lol_inf)
        print(serializer.data)
        return Response(serializer.data)


