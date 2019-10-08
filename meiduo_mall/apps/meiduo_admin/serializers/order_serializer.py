
from rest_framework import serializers
from order.models import OrderInfo,OrderGoods
from goods.models import SKU


class OrderInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = [
            'order_id',
            'create_time'
        ]

        extra_kwargs = {
            "create_time": {"format": "%Y/%m/%d"}
        }

# 自定义主表SKU序列化器
class SKUSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = [
            'name',
            'default_image'
        ]

# 自定义从表OrderGoods序列化器
class OrderGoodsModelSerializer(serializers.ModelSerializer):
    # 数据：当前OrderGoods对象关联的SKU主表对象
    # 一个
    # 序列化的结果：name\default_image
    sku = SKUSimpleSerializer()

    class Meta:
        model = OrderGoods
        fields = [
            'count',
            'price',
            'sku'
        ]

class OrderDetailModelSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    # 1、数据是什么，是什么模型类的数据？
    #       代表的数据就是：与主表对象(OrderInfo)关联的所有从表(OrderGoods)对象
    # 2、一个还是多个？
    #       多个
    # 3、序列化的结果是怎样的？
    #       count\price\sku
    skus = OrderGoodsModelSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"