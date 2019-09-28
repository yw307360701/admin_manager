from rest_framework.views import APIView
from meiduo_admin.serializers.login_serializer import *
from rest_framework.response import Response


class LoginAPIView(APIView):

    def post(self, request):
        # 1、提取前端传来对用户名和密码数据
        user_info = request.data  # {"username":xxx, "password":"xxx"}
        # 2、构建序列化器
        s = LoginSerializer(data=user_info)
        # 3、启动校验流程
        s.is_valid(raise_exception=True)
        # 4、构建响应数据
        return Response(data={
            "username": s.validated_data['user'].username,
            "user_id": s.validated_data['user'].id,
            "token": s.validated_data['token']
        })
