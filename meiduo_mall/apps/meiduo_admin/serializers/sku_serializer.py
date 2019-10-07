from rest_framework import serializers
from goods.models import SKU, SKUSpecification, GoodsCategory, SPUSpecification, SpecificationOption


class SpecOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationOption
        fields = [
            'id',
            'value'
        ]


class SPUSpesSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()

    options = SpecOptionSerializer(many=True)

    class Meta:
        model = SPUSpecification
        fields = [
            'id',
            'name',
            'spu',
            'spu_id',
            'options',
        ]


class GoodsCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = [
            'id',
            'name'
        ]


class SKUSpecModelSerializer(serializers.ModelSerializer):
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    class Meta:
        model = SKUSpecification
        fields = [
            'spec_id',
            'option_id'
        ]


class SKUModelSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField()

    # 代表的是，与当前sku主表对象关联的从表(SKUSpecification)数据集
    specs = SKUSpecModelSerializer(many=True)

    class Meta:
        model = SKU
        fields = "__all__"

    def create(self, validated_data):
        specs = validated_data.pop('specs')
        sku_obj = super().create(validated_data)
        for spec in specs:
            spec['sku_id'] = sku_obj.id
            SKUSpecification.objects.create(**spec)

        return sku_obj

    def update(self, instance, validated_data):

        specs = validated_data.pop('specs')
        instance = super().update(instance, validated_data)
        SKUSpecification.objects.filter(sku_id=instance.id).delete()
        for spec in specs:
            spec['sku_id'] = instance.id
            SKUSpecification.objects.create(**spec)

        return instance
