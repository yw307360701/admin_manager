from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings


def generate_openid_signature(openid):
    """对openid进行加密 """
    # 1.创建加密实例对象
    serializer = Serializer(secret_key=settings.SECRET_KEY, expires_in=600)

    # 2. 包装要加密的数据 {}
    data = {'openid': openid}

    # 3. 调用dumps方法进行加密  bytes
    openid_bytes = serializer.dumps(data)  # 序列化(模型转换成字典)--> 输出

    # 4. 加bytes转换成str类型
    return openid_bytes.decode()


def check_openid(openid_sign):
    """对openid进行解密"""
    # 1.创建加密实例对象
    serializer = Serializer(secret_key=settings.SECRET_KEY, expires_in=600)
    try:
        # 对openid进行解密
        data = serializer.loads(openid_sign)  # 反序列化(字典转换成模型)  ----> 输入
        # 返回openi
        return data.get('openid')
    except BadData:
        return None