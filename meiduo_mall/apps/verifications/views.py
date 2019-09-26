from django.shortcuts import render
from django.views import View
from django import http
import random


from meiduo_mall.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from meiduo_mall.utils.response_code import RETCODE
# from meiduo_mall.libs.yuntongxun.sms import CCP
from . import constants
from celery_tasks.sms.tasks import send_sms_code

import logging

logger = logging.getLogger('django')


class ImageCodeView(View):
    """图形验证码"""
    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid: 唯一标识图形验证码所属于的用户
        :return: image/jpg
        """
        # 生成图片验证码
        name, text, image = captcha.generate_captcha()

        # 保存图片验证码
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % uuid, constants.IMAGE_CODE_EXPIRE, text)

        # 响应图片验证码
        return http.HttpResponse(image, content_type='image/jpg')


class SMSCodeView(View):
    """短信验证码"""

    def get(self, reqeust, mobile):
        """
        :param reqeust: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        # 创建redis连接对象
        redis_conn = get_redis_connection('verify_code')
        # 来发短信之前先尝试性的去redis中获取此手机号60s内是否发送过短信
        send_flog = redis_conn.get('send_flog_%s' % mobile)
        # 判断是否有发送过的标记
        if send_flog:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '频繁发送短信'})
        # 接收参数
        image_code_client = reqeust.GET.get('image_code')
        uuid = reqeust.GET.get('uuid')

        # 校验参数
        if not all([image_code_client, uuid]):
            return http.JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少必传参数'})

        # 创建连接到redis的对象
        redis_conn = get_redis_connection('verify_code')
        # 提取图形验证码
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            # 图形验证码过期或者不存在
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码失效'})

        # 删除图形验证码，避免恶意测试图形验证码
        redis_conn.delete('img_%s' % uuid)

        # 对比图形验证码
        image_code_server = image_code_server.decode()  # bytes转字符串
        if image_code_client.lower() != image_code_server.lower():  # 转小写后比较
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入图形验证码有误'})

        # 生成短信验证码：生成6位数验证码
        sms_code = '%06d' % random.randint(0, 999999)

        logger.info(sms_code)
        # 管道技术
        # 创建管道 (优化，将两个储存用管道一次访问）
        pl = redis_conn.pipeline()
        # 将Redis请求添加到队列
        # 保存短信验证码
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_EXPIRE, sms_code)
        # 向redis存储一个标识,标记此手机号60s内已经发过短信
        pl.setex('send_flog_%s' % mobile, 60, '1')
        # 执行管道
        pl.execute()
        # 发送短信验证码
        # CCP().send_template_sms(mobile,[sms_code,  constants.SMS_CODE_EXPIRE // 60], 1)
        send_sms_code.delay(mobile, sms_code)
        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信成功'})
