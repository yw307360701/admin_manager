from rest_framework.viewsets import ModelViewSet
from goods.models import Brand
from meiduo_admin.serializers.brands_serializer import BrandModelSerializers
from meiduo_admin.pages import MyPage


class BrandVIewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializers
    pagination_class = MyPage