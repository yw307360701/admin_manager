from goods.models import GoodsVisitCount
from rest_framework import serializers


class GoodsVisitCountSerializer(serializers.ModelSerializer):
    # 覆盖ModelSerializer自动映射过来的类型
    category = serializers.StringRelatedField()

    class Meta:
        model = GoodsVisitCount
        fields = [
            'category',
            'count',
        ]
