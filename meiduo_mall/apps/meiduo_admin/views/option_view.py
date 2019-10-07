from rest_framework.viewsets import ModelViewSet
from meiduo_admin.pages import MyPage
from meiduo_admin.serializers.option_serializer import SpecificationOption
from rest_framework.generics import ListAPIView
from goods.models import SPUSpecification
from meiduo_admin.serializers.spec_serializer import SpecSerializer
from meiduo_admin.serializers.option_serializer import SpecOptionModelSerializer


class OptionViewSet(ModelViewSet):
    queryset = SpecificationOption.objects.all()
    serializer_class = SpecOptionModelSerializer
    pagination_class = MyPage


class SpecSimpleView(ListAPIView):
    queryset = SPUSpecification.objects.all()
    serializer_class = SpecSerializer
