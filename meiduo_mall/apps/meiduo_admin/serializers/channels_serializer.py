from rest_framework import serializers
from goods.models import GoodsChannel, GoodsChannelGroup


class GoodsChannelModelSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    group = serializers.StringRelatedField()

    # 外键关联的隐藏字段不会自动映射到序列化器的类属性中
    category_id = serializers.IntegerField()
    group_id = serializers.IntegerField()


    class Meta:
        model = GoodsChannel
        fields = [
            'id',
            'category',
            'category_id',
            'group',
            'group_id',
            'sequence',
            'url'
        ]


class GoodsChannelGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsChannelGroup
        fields = [
            'id',
            'name'
        ]