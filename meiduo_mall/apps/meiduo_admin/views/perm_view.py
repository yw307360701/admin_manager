from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.perm_serializer import *
from meiduo_admin.pages import MyPage
from rest_framework.generics import ListAPIView
from django.contrib.auth.models import *

class PermViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermModelSerializer
    pagination_class = MyPage


class ContentTypeView(ListAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContenTypeSimpleSerializer