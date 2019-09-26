from django.conf.urls import url
from . import views

urlpatterns = [
    # 注册
    url(r'^register/$', views.RegisterView.as_view(),name='register'),
    # 判断用户名是否重复注册
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view(), name='usernames'),
    # 判断手机号码是否重复
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view(), name='mobiles'),
    # 用户登录
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    # 退出登录
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    # 用户中心
    url(r'^info/$', views.UserInfoView.as_view(), name='info'),
    # 设置用户邮箱
    url(r'^emails/$', views.EmailView.as_view(), name='emails'),
    # 验证邮箱
    url(r'^emails/verification/$', views.VerifyEmailView.as_view(), name='verification'),
    # 用户地址
    url(r'^addresses/$', views.AddressView.as_view(), name='addresses'),
    # 用户新增地址
    url(r'^addresses/create/$', views.CreateAddressView.as_view(), name='c_addresses'),
    # 修改和删除地址
    url(r'^addresses/(?P<address_id>\d+)/$', views.UpdateDestroyAddressView.as_view(), name='ud_addresses'),
    # 设置默认地址
    url(r'^addresses/(?P<address_id>\d+)/default/$', views.DefaultAddressView.as_view(), name='df_addresses'),
    # 修改用户密码
    url(r'^password/$', views.ChangePasswordView.as_view(), name='password'),
    # 添加用户浏览记录
    url(r'^browse_histories/$', views.UserBrowseHistory.as_view(), name='histories'),
    # 订单显示界面
    url(r'^orders/info/(?P<page_num>\d+)/$', views.CenterOrderView.as_view()),
    # 商品评价
    url(r'^orders/comment/$', views.GoodsJudgeView.as_view()),
]