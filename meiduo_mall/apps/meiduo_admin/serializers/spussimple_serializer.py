from rest_framework import serializers
from goods.models import *


class SpuSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = (
            'id',
            'name'
        )
