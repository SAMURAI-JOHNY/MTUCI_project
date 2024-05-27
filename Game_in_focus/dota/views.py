from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from gameinfocus.models import User
from .models import DotaBlocks, UserDota
from .serializers import DotaBlocksSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class UserAPILol(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        block_id = kwargs.get('block_id')
        user = User.objects.get(pk=request.user.id)
        dota_inf = DotaBlocks.objects.get(pk=block_id)
        user_dota_inf = UserDota.objects.filter(block_id=block_id, user_id=request.user)
        if len(user_dota_inf) == 0:
            user_lol = UserDota(user_id=user, block_id=dota_inf, status=1, block_name=dota_inf.block_name,
                                course_name=dota_inf.course_name)
            user.points += 15
            user.save()
            user_lol.save()
        serializer = DotaBlocksSerializer(dota_inf)
        return Response(serializer.data)


