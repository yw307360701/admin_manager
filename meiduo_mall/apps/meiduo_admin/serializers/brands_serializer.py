from rest_framework import serializers
from goods.models import Brand


class BrandModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            # 反序列化校验后得到的是文件对象
            'logo',
            'first_letter'
        ]