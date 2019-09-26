from django.conf.urls import url
from . import views


urlpatterns = [
    # 订单结算页面
    url(r'^orders/settlement/$', views.OrderSettlementView.as_view()),
    # 订单提交
    url(r'^orders/commit/$', views.OrderCommitView.as_view()),
    # 订单成功
    url(r'^orders/success/$', views.OrderSuccessView.as_view()),
]