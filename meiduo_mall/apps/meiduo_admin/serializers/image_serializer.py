from rest_framework import serializers
from goods.models import SKUImage, SKU
from fdfs_client.client import Fdfs_client
from django.conf import settings


class ImageSerializer(serializers.ModelSerializer):
    # sku = serializers.PrimaryKeyRelatedField(queryset=SKU.objects.all())
    # 序列化：sku对象序列化成主键

    # 反序列化数据新建 SKUImage(image="group1/M00/00/02/CtM3BVrPB4GAWkTlAAGuN6wB9fU4220429", sku=sku商品对象)

    class Meta:
        model = SKUImage
        fields = [
            'id',
            'sku',
            'image'
        ]

    # def validate(self, attrs):
    #     # 把文件数据上传到fdfs
    #     # 有效数据中到image=fdfs_file_id
    #
    #     # attrs['image'] --> 文件对象
    #     file_obj = attrs['image']
    #
    #     conn = Fdfs_client(settings.FDFS_CONF_PATH)
    #     res = conn.upload_by_buffer(file_obj.read())
    #     if res['Status'] != 'Upload successed.':
    #         raise serializers.ValidationError("文件上传fdfs失败")
    #
    #     attrs['image'] = res[
    #         'Remote file_id']  # {"sku":1,  "image": "group1/M00/00/02/CtM3BVrPB4GAWkTlAAGuN6wB9fU4220429"}
    #
    #     return attrs


class SKUSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ['id', 'name']
