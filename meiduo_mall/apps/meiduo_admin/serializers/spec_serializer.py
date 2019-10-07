from rest_framework import serializers
from goods.models import SPUSpecification


class SpecSerializer(serializers.ModelSerializer):
    spu_id = serializers.IntegerField()
    spu = serializers.StringRelatedField()
    class Meta:
        model = SPUSpecification
        fields = [
            'id',
            'name',
            'spu',
            'spu_id'
        ]