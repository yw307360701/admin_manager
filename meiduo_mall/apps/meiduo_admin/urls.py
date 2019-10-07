from django.conf.urls import url
from meiduo_admin.views.login_view import LoginAPIView
from rest_framework_jwt.views import obtain_jwt_token
from meiduo_admin.views.home_view import *
from rest_framework.routers import SimpleRouter
from meiduo_admin.views.user_view import *
from meiduo_admin.views.sku_view import *
from meiduo_admin.views.spu_view import *
from meiduo_admin.views.spec_view import *
from meiduo_admin.views.option_view import *
from meiduo_admin.views.image_view import *

urlpatterns = [
    # url(r'^authorizations/$',LoginAPIView.as_view()),
    url(r'^statistical/goods_day_views/$', GoodsVisitCountView.as_view()),

    url(r'^users/$', UserAPIView.as_view()),
    url(r'^authorizations/$', obtain_jwt_token),
    # sku商品
    url(r'^skus/$', SKUViewSet.as_view({'get': 'list', 'post':'create'})),
    url(r'^skus/(?P<pk>\d+)/$', SKUViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'})),
    url(r'^skus/categories/$', SKUViewSet.as_view({'get': 'categories'})),
    url(r'^goods/simple/$', SpuSimpleView.as_view()),
    url(r'^goods/(?P<pk>\d+)/specs/$', SPUSpecSimpleVIew.as_view()),

    # spu管理
    # url(r'^goods/$', SPUViewset.as_view({'get':'list', 'post':'create'})),
    # url(r'^goods/(?P<pk>\d+)/$', SPUViewset.as_view({'get': 'retrieve',
    #                                                  'put': 'update',
    #                                                  'delete': 'destroy'})),

    url(r'^goods/brands/simple/$', BrandSimpleView.as_view()),
    url(r'^goods/channel/categories/$', GoodsCategoryView.as_view()),  # 获取一级分类信息
    url(r'^goods/channel/categories/(?P<pk>\d+)/$', GoodsCategoryView.as_view()),  # 获取二级和三级分类信息

    # 获得新建选项的可选规格
    url(r'goods/specs/simple/$', SpecSimpleView.as_view()),
    # 新增图片可选sku
    url(r'skus/simple/$', ImageViewSet.as_view({"get": "simple"})),

]


router = SimpleRouter()
router.register(prefix='statistical', viewset=HomeViewSet, base_name='home')
router.register(prefix='goods/specs', viewset=SpecViewSet, base_name='specs')
router.register(prefix='goods', viewset=SPUViewset, base_name='goods')
router.register(prefix='specs/options', viewset=OptionViewSet, base_name='options')
router.register(prefix='skus/images', viewset=ImageViewSet, base_name='images')
urlpatterns += router.urls

