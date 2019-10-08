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
from meiduo_admin.views.order_view import *
from meiduo_admin.views.perm_view import *
from meiduo_admin.views.group_view import *
from meiduo_admin.views.admin_view import *
from meiduo_admin.views.channel_view import *

urlpatterns = [
    # url(r'^authorizations/$',LoginAPIView.as_view()),
    url(r'^statistical/goods_day_views/$', GoodsVisitCountView.as_view()),

    url(r'^users/$', UserAPIView.as_view()),
    url(r'^authorizations/$', obtain_jwt_token),
    # sku商品
    url(r'^skus/$', SKUViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^skus/(?P<pk>\d+)/$', SKUViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
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

    # 订单
    url(r'orders/$', OrderInfoView.as_view()),
    url(r'orders/(?P<pk>\d+)/$', OrderInfoView.as_view()),
    url(r'orders/(?P<pk>\d+)/status/$', OrderInfoView.as_view()),

    # 权限管理
    url(r'permission/perms/$', PermViewSet.as_view({"get": "list", "post": 'create'})),
    url(r'permission/perms/(?P<pk>\d+)/$', PermViewSet.as_view({"get": "retrieve",
                                                                "delete": "destroy",
                                                                "put": "update"})),
    # 新增权限可选类型
    url(r'permission/content_types/$', ContentTypeView.as_view()),

    # 分组管理
    url(r'permission/groups/$', GroupViewSet.as_view({"get": "list", 'post': "create"})),
    url(r'permission/groups/(?P<pk>\d+)/$', GroupViewSet.as_view({"get": "retrieve",
                                                                  "put": "update",
                                                                  "delete": "destroy"})),
    # 新增分组可选权限
    url(r'permission/simple/$', GroupPermView.as_view()),

    # 管理员权限
    url(r'permission/admins/$', AdminView.as_view({'get': 'list', 'post': 'create'})),
    url(r'permission/admins/(?P<pk>\d+)/$', AdminView.as_view({"get": "retrieve",
                                                               "put": "update",
                                                               "delete": "destroy"})),
    # 新增管理员可选分组
    url(r'permission/groups/simple/$', AdminGroupView.as_view()),
    # 频道管理
    url(r'goods/channels/$', GoodsChannelViewSet.as_view({'get': 'list'})),

]

router = SimpleRouter()
router.register(prefix='statistical', viewset=HomeViewSet, base_name='home')
router.register(prefix='goods/specs', viewset=SpecViewSet, base_name='specs')
router.register(prefix='goods', viewset=SPUViewset, base_name='goods')
router.register(prefix='specs/options', viewset=OptionViewSet, base_name='options')
router.register(prefix='skus/images', viewset=ImageViewSet, base_name='images')
urlpatterns += router.urls
