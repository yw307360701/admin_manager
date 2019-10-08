from rest_framework.viewsets import ModelViewSet
from goods.models import GoodsChannel
from meiduo_admin.pages import MyPage
from meiduo_admin.serializers.channels_serializer import GoodsChannelModelSerializer


class GoodsChannelViewSet(ModelViewSet):
    queryset = GoodsChannel.objects.all()
    serializer_class = GoodsChannelModelSerializer
    pagination_class = MyPage