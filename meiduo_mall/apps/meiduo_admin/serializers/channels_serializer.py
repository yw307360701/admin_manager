from rest_framework import serializers
from goods.models import GoodsChannel


class GoodsChannelModelSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    group = serializers.StringRelatedField()

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

