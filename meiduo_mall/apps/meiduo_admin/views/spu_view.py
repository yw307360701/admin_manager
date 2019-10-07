from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from goods.models import SPU,Brand, GoodsCategory
from meiduo_admin.serializers.spu_serializer import *
from meiduo_admin.pages import MyPage


class SPUViewset(ModelViewSet):
    queryset = SPU.objects.all()
    serializer_class = SPUModelserializer
    pagination_class = MyPage


class BrandSimpleView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrnadSimpleserializer


class GoodsCategoryView(ListAPIView):
    queryset = GoodsCategory.objects.all()
    serializer_class = GoodsCategorySimpleserializer

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        if category_id:
            return GoodsCategory.objects.filter(parent_id=category_id)
        return self.queryset.filter(parent=None)