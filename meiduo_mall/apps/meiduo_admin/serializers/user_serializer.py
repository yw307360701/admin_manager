from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password


# 定义一个序列化器，序列化处理User模型类对象


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'mobile',
            'email',

            'password',
        ]

    # def validate(self, attrs):
    #     # 1、密码加密
    #     password = attrs.get("password") # 12345678
    #     attrs['password'] = make_password(password) # pbkdf2_sha256$36000$Gkac4k0CnrUP$7Bx3aDCTvQG19gvivTgxHyvlBGochfctljOMTyKVcSk=
    #     # 2、添加is_staff=True
    #     attrs['is_staff'] = True
    #     return attrs

    # def create(self, validated_data):
    #     # validated_data = {"password": "12345678"} # {"is_staff": True}
    #     # 1、密码加密
    #     password = validated_data.get("password") # 12345678
    #     validated_data['password'] = make_password(password) # pbkdf2_sha256$36000$Gkac4k0CnrUP$7Bx3aDCTvQG19gvivTgxHyvlBGochfctljOMTyKVcSk=
    #     # 2、添加is_staff=True
    #     validated_data['is_staff'] = True
    #
    #     return self.Meta.model.objects.create(**validated_data)

    def create(self, validated_data):
        # validated_data: 明文密码，没有is_staff=True
        # User.objects.create_user(**validated_data) # 将密码加密
        return User.objects.create_superuser(**validated_data)  # 密码加密，设置超级管理员
