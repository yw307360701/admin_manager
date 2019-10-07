from meiduo_admin.pages import MyPage
from rest_framework.viewsets import ModelViewSet
from goods.models import SPUSpecification
from meiduo_admin.serializers.spec_serializer import *


class SpecViewSet(ModelViewSet):
    queryset = SPUSpecification.objects.all()
    serializer_class = SpecSerializer
    pagination_class = MyPage