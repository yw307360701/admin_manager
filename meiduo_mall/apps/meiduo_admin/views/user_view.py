from rest_framework.generics import ListAPIView, CreateAPIView
from users.models import User
from meiduo_admin.serializers.user_serializer import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from meiduo_admin.pages import MyPage


class UserAPIView(ListAPIView, CreateAPIView):
    # select * from tb_user where is_staff=1;
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserModelSerializer
    pagination_class = MyPage

    def get_queryset(self):
        # 根据查询字符串中的keyword进行过滤
        # 1、获得这个keyword（查询字符串参数）
        keyword = self.request.query_params.get("keyword")
        # 2、过滤
        if keyword:
            return self.queryset.filter(username__contains=keyword)

        # select * from tb_user where is_staff=1;
        return self.queryset.all()  # 更新数据集
