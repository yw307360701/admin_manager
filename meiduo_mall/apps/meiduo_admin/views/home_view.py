from rest_framework.views import APIView
from users.models import User
from rest_framework.response import Response
from django.utils import timezone
import pytz
from django.conf import settings
from datetime import timedelta
from order.models import OrderInfo
from rest_framework.decorators import action

from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView
from goods.models import GoodsVisitCount
from meiduo_admin.serializers.home_serializer import *


class HomeViewSet(ViewSet):

    @action(methods=['get'], detail=False)  # , url_path='total_count')
    def total_count(self, request):
        # 1、获得用户数据集
        user_queryset = User.objects.all()
        # 2、统计个数
        count = user_queryset.count()

        # 3、构建响应
        # UTC时间(零时区时)：2019年9月26日 2时15分56秒 零时区
        utc_time = timezone.now()
        # 本地时间：2019年9月26日 10时15分56秒 上海（东八区）
        local_time = utc_time.astimezone(tz=pytz.timezone(settings.TIME_ZONE))

        return Response({
            "count": count,
            "date": local_time.date()
        })

    @action(methods=['get'], detail=False)
    def day_increment(self, request):
        # 统计当天新增用户，过滤
        # 1、已知条件： 当日的零时
        # 2、目标数据： 用户对象
        # 思考：本表已知条件查询本表数据

        # 1、获得当日的零时
        utc_time = timezone.now()
        # 2019/9/26 10:33:56.321421 +8:06
        local_time = utc_time.astimezone(tz=pytz.timezone(settings.TIME_ZONE))
        # 2019/9/26 0:0:0.00000 +8:06
        local_0_time = local_time.replace(hour=0, minute=0, second=0, microsecond=0)
        # 2、根据零时过滤用户对象
        count = User.objects.filter(date_joined__gte=local_0_time).count()
        # 3、返回响应
        return Response({
            "count": count,
            "date": local_time.date()
        })

    @action(methods=['get'], detail=False)
    def day_active(self, request):
        # 当日活跃用户
        local_0_time = timezone.now().astimezone(tz=pytz.timezone(settings.TIME_ZONE)). \
            replace(hour=0, minute=0, second=0)

        count = User.objects.filter(last_login__gte=local_0_time).count()

        return Response({
            "count": count,
            "date": local_0_time.date()
        })

    @action(methods=['get'], detail=False)
    def day_orders(self, request):
        # 统计当日下单的用户数量
        # 1、已知条件：当日零时
        # 2、目标数据：用户对象
        # 思考：已知条件是订单表(从)，目标数据是用户表(主)
        # 从表已知条件，查询主表数据

        local_0_time = timezone.now().astimezone(tz=pytz.timezone(settings.TIME_ZONE)). \
            replace(hour=0, minute=0, second=0)

        # # 方案一：从表入手查询
        # # 当日下的订单
        # user_list = []
        # order_queryset = OrderInfo.objects.filter(create_time__gte=local_0_time)
        # for order in order_queryset:
        #     # order: 单一的订单对象
        #     user_list.append(order.user)
        # # user_list：当日下单的用户对象
        # count = len(set(user_list))
        # return Response({
        #     "count": count,
        #     "date": local_0_time.date()
        # })

        # 方案二：从主表入手
        user_queryset = User.objects.filter(orderinfo__create_time__gte=local_0_time)
        count = len(set(user_queryset))
        return Response({
            "count": count,
            "date": local_0_time.date()
        })

    @action(methods=['get'], detail=False)
    def month_increment(self, request):
        # 统计最近30天中每一天的日增用户(包括当日)
        # 已知条件：每一天的零点
        # 查询数据：用户对象

        # 日期范围
        # 起始日期的零时：当日减去29天
        # 最后一天零时：2019/9/26 0：0：0

        # 单日零时
        cur_0_time = timezone.now().astimezone(tz=pytz.timezone(settings.TIME_ZONE)). \
            replace(hour=0, minute=0, second=0)
        # 近30天的起始日期零时
        start_0_time = cur_0_time - timedelta(days=29)

        user_list = []
        for index in range(30):
            # 第一次遍历计算日期：  start_0_time+timedelta(days=0)， index=0
            # 第二次：           start_0_time+timedelta(days=1),  index=1
            # 第三次：           start_0_time+timedelta(days=2),  index=2
            # 第n次：            start_0_time+timedelta(days=index)
            # 用于计算的某一天的零时
            calc_0_time = start_0_time + timedelta(days=index)
            next_0_time = calc_0_time + timedelta(days=1)
            count = User.objects.filter(date_joined__gte=calc_0_time, date_joined__lt=next_0_time).count()
            user_list.append({
                "count": count,
                "date": calc_0_time.date()
            })

        return Response(user_list)


class GoodsVisitCountView(ListAPIView):
    # 该视图序列化返回的目标数据集，并不是所有对象
    # 而是创建时间是当日的对象

    # local_0_time = timezone.now().astimezone(tz=pytz.timezone(settings.TIME_ZONE)). \
    #         replace(hour=0, minute=0, second=0)
    # queryset = GoodsVisitCount.objects.filter(create_time__gte=local_0_time)

    queryset = GoodsVisitCount.objects.all()
    serializer_class = GoodsVisitCountSerializer

    def get_queryset(self):
        # 获得0时，然后过滤出当日访问量对象
        local_0_time = timezone.now().astimezone(tz=pytz.timezone(settings.TIME_ZONE)). \
            replace(hour=0, minute=0, second=0)

        return self.queryset.filter(create_time__gte=local_0_time)
