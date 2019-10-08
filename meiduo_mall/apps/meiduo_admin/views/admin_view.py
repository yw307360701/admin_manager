from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.admin_serializser import *
from meiduo_admin.pages import MyPage
from rest_framework.generics import ListAPIView


class AdminView(ModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = AdminSerializer
    pagination_class = MyPage


class AdminGroupView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = AdminGroupSimlieSerializer