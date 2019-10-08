from rest_framework.mixins import ListModelMixin,RetrieveModelMixin,UpdateModelMixin
from rest_framework.generics import GenericAPIView
from order.models import *
from meiduo_admin.serializers.order_serializer import *
from meiduo_admin.pages import MyPage



from rest_framework.permissions import BasePermission

# 自定义一个权限，只有拥有吃饭这个权限才能访问当前视图
class CanChiFan(BasePermission):
    """
    验证用户是否有吃饭这个权限
    """
    def has_permission(self, request, view):
        return request.user and request.user.has_perm("users.chifan")



class OrderInfoView(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = OrderInfo.objects.all()
    serializer_class = OrderInfoModelSerializer
    pagination_class = MyPage

    # permission_classes = [CanChiFan]

    def get_queryset(self):
        # 在非视图函数中，获得查询字符串参数
        keyword = self.request.query_params.get("keyword")
        if keyword:
            return self.queryset.filter(order_id__contains=keyword)

        return self.queryset.all()

    def get_serializer_class(self):
        if self.kwargs.get('pk'):
            return OrderDetailModelSerializer
        return self.serializer_class

    def get(self, request, *args, **kwargs):
        # 调用list --> 序列化返回多条
        # 调用retrieve --> 根据pk过滤单一返回
        order_id = kwargs.get('pk')
        if order_id:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

