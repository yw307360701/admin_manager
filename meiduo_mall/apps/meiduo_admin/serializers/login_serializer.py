# 自定义序列化器
# 1、对username和password进行有效校验
# 2、生成token

from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True, max_length=100)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']

        # 1、进行传统身份认证
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("传统身份校验失败！")

        # 2、如果通过，生成token
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # 3、返回有效数据
        return {
            "user": user,
            "token": token
        }
