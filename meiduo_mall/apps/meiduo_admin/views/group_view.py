from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group
from meiduo_admin.serializers.group_serializser import GroupModelSerializer
from meiduo_admin.pages import MyPage
from rest_framework.generics import ListAPIView
from meiduo_admin.serializers.perm_serializer import *


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    pagination_class = MyPage


class GroupPermView(ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermModelSerializer