from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.sku_serializer import *
from goods.models import SKU, GoodsCategory
from meiduo_admin.pages import MyPage
from rest_framework.response import Response


class SKUViewSet(ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SKUModelSerializer
    pagination_class = MyPage

    def get_queryset(self):
        # 判断如果处理请求的视图函数是categories，那么应该返回三级分类查询集
        # 视图对象.action属性：处理请求的视图函数的名称
        if self.action == "categories":
            return GoodsCategory.objects.filter(parent_id__gt=37)

        # 原来的逻辑
        keyword = self.request.query_params.get("keyword")
        if keyword:
            return self.queryset.filter(name__contains=keyword)
        return self.queryset.all()

    def get_serializer_class(self):
        # 如果处理请求的视图是categories，返回GoodsCategoryDetailSerializer
        if self.action == "categories":
            return GoodsCategoryDetailSerializer

        return self.serializer_class

    def categories(self, request):
        # 序列化返回三级分类信息
        # 1、获得三级分类对象查询集
        category_3_queryset = self.get_queryset()
        # 2、构建序列化器对象
        s = self.get_serializer(category_3_queryset, many=True)
        # 3、序列化返回
        return Response(s.data)
