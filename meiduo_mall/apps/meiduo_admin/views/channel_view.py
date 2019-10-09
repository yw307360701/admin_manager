from rest_framework.viewsets import ModelViewSet
from meiduo_admin.pages import MyPage
from meiduo_admin.serializers.channels_serializer import *
from rest_framework.response import Response
from rest_framework.decorators import action


class GoodsChannelViewSet(ModelViewSet):
    queryset = GoodsChannel.objects.all()
    serializer_class = GoodsChannelModelSerializer
    pagination_class = MyPage

    @action(methods=['get'], detail=False)
    def channel_types(self, request):
        channel_groups = GoodsChannelGroup.objects.all()
        s = GoodsChannelGroupSerializer(channel_groups,many=True)
        return Response(s.data)

