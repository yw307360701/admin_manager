from django.conf.urls import url
from . import views


urlpatterns = [
    # 购物车增，删，改，查
    url(r'^carts/$', views.CartsView.as_view()),
    # 购物车全选
    url(r'^carts/selection/$', views.CartsSelectAllView.as_view()),
    # 购物车装简单版展示
    url(r'^carts/simple/$', views.CartsSimpleView.as_view()),
]