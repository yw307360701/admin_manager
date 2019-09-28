from django.conf.urls import url
from meiduo_admin.views.login_view import LoginAPIView
from rest_framework_jwt.views import obtain_jwt_token
from meiduo_admin.views.home_view import *
from rest_framework.routers import SimpleRouter
from meiduo_admin.views.user_view import *
from meiduo_admin.views.sku_view import *

urlpatterns = [
    # url(r'^authorizations/$',LoginAPIView.as_view()),
    url(r'^statistical/goods_day_views/$', GoodsVisitCountView.as_view()),

    url(r'^users/$', UserAPIView.as_view()),
    url(r'^authorizations/$', obtain_jwt_token),
    # sku商品
    url(r'^skus/$', SKUViewSet.as_view({'get': 'list'})),
    url(r'^skus/categories/$', SKUViewSet.as_view({'get': 'categories'})),
]


router = SimpleRouter()
router.register(prefix='statistical', viewset=HomeViewSet, base_name='home')
urlpatterns += router.urls

