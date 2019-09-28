from django.contrib.auth.backends import ModelBackend
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings

from .models import User


def get_user_by_account(account):
    """
    根据account查询用户
    :param account:mobile/username
    :return:user
    """
    try:

        if re.match(r'^1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
        return user
    except User.DoesNotExist:
        return None


class UsernameMobileAuthBackend(ModelBackend):
    """自定义认证后端实现多账号登录"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        # # 1.根据用户名或手机号 查询user
        # user = get_user_by_account(username)
        # # 2.校验用户密码
        # if user and user.check_password(password) and user.is_active:
        #     # 返回user or None
        #     return user
        try:

            user = User.objects.get(username=username)
        except:
            # 如果未查到数据，则返回None，用于后续判断
            try:
                user = User.objects.get(mobile=username)
            except:
                return None

            # 如果该请求是来自后台管理站点的登陆请求
            # 那么就需要验证用户是否是超级管理员
            # 关键问题：根据request对象是否为空，来判断此次登陆请求是否是后台站点登陆
        if request is None:
            # 后台站点登陆
            if not user.is_staff:
                return None

            # 判断密码
        if user.check_password(password):
            return user
        else:
            return None


def generate_verify_email_url(user):
    """用来激活邮箱的url"""
    # 创建加密实例对象
    serializer = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600*24)
    # 包装要加密的字典数据
    data = {'user_id': user.id, 'email': user.email}
    # 加密decode（）
    token = serializer.dumps(data).decode()
    # 包装激活url
    verify_url = settings.EMAIL_VERIFY_URL + '?token=' + token
    # 返回url
    return verify_url


def check_verify_email_token(token):
    """
    对token进行解密并返回指定user
    :param token: 要解密的字段
    :return: user or None
    """
    # 创建要解密的实例对象
    serializer = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600*24)
    # loads
    try:
        data = serializer.loads(token)
        user_id = data.get('user_id')
        email = data.get('email')
        try:
            user = User.objects.get(id=user_id, email=email)
            return user
        except User.DoesNotExist:
            return None
    except BadData:
        return None