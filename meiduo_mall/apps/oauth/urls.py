from django.conf.urls import url

from . import views


urlpatterns = [
    # 获取QQ登录url
    url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
    # QQ登录成功后回调处理
    url(r'^oauth_callback$', views.QQAuthView.as_view()),
]