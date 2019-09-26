import pickle, base64
from django_redis import get_redis_connection


def merge_cart_cookie_to_redis(request, response):
    """合并购物车"""

    # 获取cookie购物车数据
    cart_str = request.COOKIES.get('cart')
    # 判断是否有cookie购物车数据
    # 如果没有提前return
    if cart_str is None:
        return

    # 将cart_str 转换成 cart_dict
    cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
    redis_conn = get_redis_connection('carts')
    user = request.user
    # 遍历cookie大字典
    for sku_id in cart_dict:
        # 将sku_id及count向redis的hash中添加
        redis_conn.hset('cart_%s' % user.id, sku_id, cart_dict[sku_id]['count'])
        # 判断当前sku_id是勾选还是未勾选
        if cart_dict[sku_id]['selected']:
            # 如果勾选就将当前sku_id添加到set中
            redis_conn.sadd('selected_%s' % user.id, sku_id)
        else:
            # 如果未勾选就将当前sku_id从set中移除
            redis_conn.srem('selected_%s' % user.id, sku_id)

    # 删除cookie购物车数据
    response.delete_cookie('carts')

