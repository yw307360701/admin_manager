from rest_framework.viewsets import ModelViewSet
from meiduo_admin.pages import MyPage
from meiduo_admin.serializers.image_serializer import *
from rest_framework.response import Response
from rest_framework.decorators import action


class ImageViewSet(ModelViewSet):
    queryset = SKUImage.objects.all()
    serializer_class = ImageSerializer
    pagination_class = MyPage

    # skus/simple
    @action(methods=['get'], detail=False)
    def simple(self, request):
        # 序列化返回可选sku信息
        sku_queryset = SKU.objects.all()
        s = SKUSimpleSerializer(sku_queryset, many=True)
        return Response(s.data)
