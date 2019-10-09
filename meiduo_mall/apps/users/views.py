from django.shortcuts import render, redirect
from django.views import View
from django import http
import re
from django.contrib.auth import login, authenticate, logout
from django_redis import get_redis_connection
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
import json
from django.db import DatabaseError
from decimal import Decimal
from django.core.paginator import Paginator, EmptyPage

from .models import User, Address
from goods.models import SKU
from meiduo_mall.utils.response_code import RETCODE
from meiduo_mall.utils.views import LoginRequiredView
from celery_tasks.email.tasks import send_verify_email
from .utils import generate_verify_email_url, check_verify_email_token
import logging
from cats.utils import merge_cart_cookie_to_redis
from order.models import OrderInfo, OrderGoods

logger = logging.getLogger('django')


class RegisterView(View):
    """注册"""

    def get(self, request):

        return render(request, 'register.html')

    def post(self, request):
        # 1.接收请求体表单数据  POST
        query_dict = request.POST
        username = query_dict.get('username')
        password = query_dict.get('password')
        password2 = query_dict.get('password2')
        mobile = query_dict.get('mobile')
        sms_code = query_dict.get('sms_code')
        allow = query_dict.get('allow')  # 如果表单复选框没有指定value时，传入的是'on'，反之传入None

        # 2.校验数据
        if all([username, password, password2, mobile, sms_code, allow]) is False:
            return http.HttpResponseForbidden('缺少必传参数')

        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')

        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        if password != password2:
            return http.HttpResponseForbidden('输入两次密码不一致')

        if not re.match(r'^1[345789]\d{9}$', mobile):
            return http.HttpResponseForbidden('您输入的手机号格式不正确')

        # 创建连接到redis的对象
        redis_conn = get_redis_connection('verify_code')
        # 提短信验证码
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            # 短信验证码过期或者不存在
            return http.JsonResponse({'code': RETCODE.SMSCODERR, 'errmsg': '短信验证码失效'})

        # 删除短信验证码，避免恶意测试短信验证码
        redis_conn.delete('sms_%s' % mobile)

        # 对比短信验证码
        sms_code_server = sms_code_server.decode()  # bytes转字符串
        if sms_code != sms_code_server.lower():  # 转小写后比较
            return http.JsonResponse({'code': RETCODE.SMSCODERR, 'errmsg': '输入短信验证码有误'})

        # 创建user并且存储到表中
        user = User.objects.create_user(username=username, password=password, mobile=mobile)

        # 用户注册成功代表登陆成功（状态保持）
        login(request, user)

        # 创建响应对象
        response = redirect('/')
        # 用户登录成功后向cookie中存储username
        response.set_cookie('username', user.username, max_age=settings.SESSION_COOKIE_AGE)
        # 响应
        # return http.HttpResponse('注册成功，应该去到首页')
        return response


class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param request: 请求对象
        :param username: 用户名
        :return: JSON
        """
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class MobileCountView(View):
    """判断手机号是否重复注册"""

    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class LoginView(View):
    """用户名登录"""

    def get(self, request):
        """
        提供登录界面
        :param request: 请求对象
        :return: 登录界面
        """
        return render(request, 'login.html')

    def post(self, request):
        """
        实现登录逻辑
        :param request: 请求对象
        :return: 登录结果
        """
        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')

        # 认证登录用户
        if all([username, password]) is False:
            return http.HttpResponseForbidden('缺少必传参数')

        user = authenticate(username=username, password=password)

        # 判断用户是否通过认证
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误'})

        # 实现状态保持
        login(request, user)
        # 设置状态保持的周期
        request.session.set_expiry(None if remembered else 0)
        # 获取用户来源
        next = request.GET.get('next')  # 取到返回next=info，没有返回None
        # 创建响应对象
        response = redirect(next or '/')
        # 用户登录成功后向cookie中存储username
        response.set_cookie('username', user.username, max_age=settings.SESSION_COOKIE_AGE)
        # 登录成功合并购物车
        merge_cart_cookie_to_redis(request, response)
        # 响应登录结果
        # return http.HttpResponse('登录成功， 跳转到首页界面')
        return response


class LogoutView(View):
    """退出登录"""

    def get(self, request):
        """实现退出登录逻辑"""

        # 清楚状态保持
        logout(request)
        # 退出登录，重定向到登录界面
        response = redirect('users:login')
        # 退出登录时清除cookie中的username
        response.delete_cookie('username')
        return response


# class UserInfoView(View):
#     """用户中心"""
#
#     def get(self, request):
#         user = request.user
#         # 如果是登录用户，就展示用户中心界面
#         if user.is_authenticated:
#             return render(request, 'user_center_info.html')
#         else:
#             # 如果是没登录，重定向到首页
#             return redirect('/login/?next=/info/')

class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_center_info.html')


class EmailView(LoginRequiredView):
    """设置用户邮箱,并发送激活邮箱url"""

    def put(self, request):
        # 1.接收请求体非表单数据 body
        json_dict = json.loads(request.body.decode())
        email = json_dict.get('email')

        # 2.校验
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('邮箱格式有误')

        # 3.修改user模型的email字段

        user = request.user
        # 如果用户还没有设置邮箱再去设置,如果设置过了就不要再设置了
        if user.email != email:
            user.email = email
            user.save()

        # 给当前设置的邮箱发一封激活url
        # 给当前设置的邮箱发一封激活url
        # send_mail(subject='邮件的标题/主题', message='普通字符串邮件正文', from_email='发件人', recipient_list=['收件人邮箱'],
        # html_message='超文本邮件正文')
        # html_message = '<p>这是一个激活邮件 <a href="http://www.baidu.com">点我一下<a></p>'
        # send_mail(subject='激活邮箱', message='普通字符串邮件正文', from_email='美多商城<itcast99@163.com>', recipient_list=[email],
        #           html_message=html_message)
        # 异步发送短信
        verify_url = generate_verify_email_url(user)
        send_verify_email.delay(email, verify_url)

        # 响应
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '添加邮箱成功'})


class VerifyEmailView(View):
    """验证邮箱"""

    def get(self, request):
        # 接收查询参数中的token
        token = request.GET.get('token')

        # 对token解密 并根据用户信息查询到指定user
        user = check_verify_email_token(token)
        if user is None:
            return http.HttpResponseForbidden('邮箱激活失败')
        # 修改指定user中的email_active字段
        user.email_active = True
        user.save()
        # 响应
        return render(request, 'user_center_info.html')


class AddressView(LoginRequiredView):
    """用户收货地址"""

    def get(self, request):
        """提供收货地址界面"""
        # return render(request, 'user_center_site.html')
        user = request.user
        # 将当前登录用户的所有未被逻辑删除的收货地址全部查询出来
        address_qs = Address.objects.filter(user=user, is_deleted=False)
        # user.addresses.filter(is_deleted=False)
        # 对查询集中的每个address模型对象转换成字典并包装到列表中
        address_list = []  # 用来装收货地址字典
        for address in address_qs:
            address_list.append({
                'id': address.id,
                'title': address.title,
                'receiver': address.receiver,
                'province_id': address.province_id,
                'province': address.province.name,
                'city_id': address.city_id,
                'city': address.city.name,
                'district_id': address.district_id,
                'district': address.district.name,
                'place': address.place,
                'mobile': address.mobile,
                'tel': address.tel,
                'email': address.email
            })

        context = {
            'addresses': address_list,
            'default_address_id': user.default_address_id
        }
        return render(request, 'user_center_site.html', context)


class CreateAddressView(LoginRequiredView):
    """新增收货地址"""

    def post(self, request):

        # 1. 接收请求体非表单数据 body
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 2. 校验
        if all([title, receiver, province_id, city_id, district_id, place, mobile]) is False:
            return http.HttpResponseForbidden('缺少必传参数')

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('参数mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseForbidden('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseForbidden('参数email有误')
        # 新增地址成功，将新增的地址响应给前端实现局部刷新
        try:
            address = Address.objects.create(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
        except DatabaseError as e:
            logger.error(e)
            return http.HttpResponseForbidden('新增收货地址出错')
        user = request.user
        # 判断当前用户是否有默认地址，没有默认地址给用户设置一个默认地址
        if user.default_address is None:
            # 给用户这是默认地址
            user.default_address = address
            user.save()

        # 4.将新增好的Address模型对象转换成字典
        address_dict = {
            'id': address.id,
            'title': address.title,
            'receiver': address.receiver,
            'province_id': address.province_id,
            'province': address.province.name,
            'city_id': address.city_id,
            'city': address.city.name,
            'district_id': address.district_id,
            'district': address.district.name,
            'place': address.place,
            'mobile': address.mobile,
            'tel': address.tel,
            'email': address.email
        }

        # 响应
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '新增地址成功', 'address': address_dict})


class UpdateDestroyAddressView(LoginRequiredView):
    """修改和删除用户地址"""

    def put(self, request, address_id):
        user = request.user
        try:
            address = Address.objects.get(id=address_id, user=user, is_deleted=False)
        except Address.DoesNotExist:
            return http.HttpResponseForbidden('address_id有误')

        # 1.接收请求体非表单数据 body
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 2. 校验
        if all([title, receiver, province_id, city_id, district_id, place, mobile]) is False:
            return http.HttpResponseForbidden('缺少必传参数')

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('手机号格式有误')

        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseForbidden('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseForbidden('参数email有误')

        try:
            # 3.创建Address模型对象并保存数据
            address = Address.objects.create(
                user=user,
                title=title,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
        except DatabaseError as e:
            logger.error(e)
            return http.HttpResponseForbidden('新增收货地址错误')

        # 3.修改用户收货地址
        address.title = title
        address.receiver = receiver
        address.province_id = province_id
        address.city_id = city_id
        address.district_id = district_id
        address.place = place
        address.mobile = mobile
        address.tel = tel
        address.email = email
        address.save()

        # 4.将新增好的address模型对象转换成字典
        address_dict = {
            'id': address.id,
            'title': address.title,
            'receiver': address.receiver,
            'province_id': address.province_id,
            'province': address.province.name,
            'city_id': address.city_id,
            'city': address.city.name,
            'district_id': address.district_id,
            'district': address.district.name,
            'place': address.place,
            'mobile': address.mobile,
            'tel': address.tel,
            'email': address.email
        }

        # 响应
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '修改收货地址成功', 'address': address_dict})

    def delete(self, request, address_id):
        """删除地址"""
        try:
            # 查询要删除的地址
            address = Address.objects.get(id=address_id)
            # 将地址逻辑删除设置为True
            address.is_deleted = True
            address.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '删除地址失败'})
            # 显示删除地址结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '删除地址成功'})


class DefaultAddressView(LoginRequiredView):
    """设置默认地址"""

    def put(self, request, address_id):
        user = request.user
        try:
            # 接收地址， 查询地址
            address = Address.objects.get(id=address_id)
        except Exception as e:
            return http.HttpResponseForbidden('address_id有误')
        # 设置默认地址
        user.default_address = address
        user.save()
        # 响应默认地址结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '设置默认地址成功'})


class ChangePasswordView(LoginRequiredView):
    """修改用户密码"""

    def get(self, request):

        return render(request, 'user_center_pass.html')

    def post(self, request):

        # 接收表单数据
        query_dict = request.POST
        old_pwd = query_dict.get('old_pwd')
        new_pwd = query_dict.get('new_pwd')
        new_cpwd = query_dict.get('new_cpwd')
        # 校验
        if all([old_pwd, new_pwd, new_cpwd]) is False:
            return http.HttpResponseForbidden('缺少必传参数')
        user = request.user
        if user.check_password(old_pwd) is False:
            return render(request, 'user_center_pass.html', {'origin_pwd_errmsg': '原始密码错误'})
        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_pwd):
            return http.HttpResponseForbidden('密码最少8位，最长20位')
        if new_pwd != new_cpwd:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 修改用户password密码，加密后再存储
        user.set_password(new_pwd)
        user.save()

        # 清除状态保持
        logout(request)
        response = redirect('/login/')
        # 将cookie中的username清楚
        response.delete_cookie('username')
        # 重定向到login界面
        return response


class UserBrowseHistory(View):
    """用户浏览记录"""

    def post(self, request):
        """保存浏览记录"""

        # user = request.user
        # if not user.is_authenticated:
        #     return http.JsonResponse({'code': RETCODE.SMSCODERR, 'errmsg': '未登录用户不能添加浏览记录'})
        # # 接收
        # json_dict = json.loads(request.body.decode())
        # sku_id = json_dict.get('sku_id')
        # try:
        #     sku_id = SKU.objects.get(id=sku_id, is_launched=True)
        # except SKU.DoesNotExist:
        #     return http.HttpResponseForbidden('sku_id不存在')
        user = request.user
        # 如果用户没有登录直接提前响应
        if not user.is_authenticated:
            return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '未登录用户不能添加浏览记录'})
        # 接收
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')

        # 校验
        try:
            sku_model = SKU.objects.get(id=sku_id, is_launched=True)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden('sku_id不存在')

        # 创建redis连接对象
        redis_conn = get_redis_connection('history')

        # redis_conn = get_redis_connection('history')

        # 接收用户redis中列表的key
        key = 'history_%s' % user.id
        pl = redis_conn.pipeline()
        # 先去重
        pl.lrem(key, 0, sku_id)
        # 添加到列表中开头
        pl.lpush(key, sku_id)
        # 截取列表中前5个元素
        pl.ltrim(key, 0, 4)
        # 执行管道
        pl.execute()

        # 响应
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})

    def get(self, request):

        user = request.user

        if not user.is_authenticated:
            return http.JsonResponse({'code': RETCODE.SERVERERR, 'errmsg': '未登录用户不能获取浏览记录'})

        redis_conn = get_redis_connection('history')

        sku_ids = redis_conn.lrange('history_%s' % user.id, 0, -1)

        sku_list = []  # 用来装每一个sku字典
        for sku_id in sku_ids:
            # 查询sku模型
            sku_model = SKU.objects.get(id=sku_id)
            # sku模型转换成字典
            sku_list.append(
                {
                    'id': sku_model.id,
                    'default_image_url': sku_model.default_image.url,
                    'name': sku_model.name,
                    'price': sku_model.price
                }
            )

        # 响应
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'skus': sku_list})


class CenterOrderView(LoginRequiredView):
    """订单显示"""

    def get(self, request, page_num):
        # 获取登录用户
        user = request.user
        # 获取当前登录用户的所有订单
        query_dict = OrderInfo.objects.filter(user=user)
        page_orders = []
        for order in query_dict:
            sku_list = []
            goods_dict = OrderGoods.objects.filter(order=order)
            for goods in goods_dict:
                sku = SKU.objects.get(id=goods.sku_id)
                sku_list.append({
                    'name': sku.name,
                    'price': sku.price,
                    'default_image': sku.default_image,
                    'count': goods.count,
                    'amount': goods.price,
                })

            page_orders.append({
                'create_time': order.create_time,
                'order_id': order.order_id,
                'sku_list': sku_list,
                'total_amount': order.total_amount,
                'freight': Decimal('10.00'),
                'pay_method_name': order.PAY_METHOD_CHOICES[order.pay_method - 1][1],
                'status_name': order.ORDER_STATUS_CHOICES[order.status - 1][1],
                'status': order.status,
            })
        # 创建分页器 (要分页的所有数据, 每页显示多少条数据)
        paginator = Paginator(page_orders, 5)
        total_page = paginator.num_pages  # 获取总页数
        try:
            page_skus = paginator.page(page_num)  # 获取指定页的数据
        except EmptyPage:
            return http.HttpResponseForbidden('没有指定页')

        context = {
            'page_num': page_num,
            'page_orders': page_skus,
            'total_page': total_page,
        }

        return render(request, 'user_center_order.html', context)


class GoodsJudgeView(LoginRequiredView):
    """商品评价"""

    def get(self, request):

        # 获取order_id
        # query_dict =
        order_id = request.GET.get('order_id')
        # user = request.user
        # 校验order_id是否真实有效
        # try:
        #     order = OrderInfo.objects.get(order_id=order_id)
        # except OrderInfo.DoesNotExist:
        #     return http.HttpResponseForbidden('order_id不存在')
        # order = OrderInfo.objects.get(order_id=order_id)
        skus = []
        order_qs= OrderGoods.objects.filter(order_id=order_id, is_commented=False)
        for order in order_qs:
            sku = SKU.objects.get(id=order.sku_id)
            skus.append({
                'default_image_url': sku.default_image.url,
                'name': sku.name,
                'price': str(sku.price),
                'url': sku.id,
                'display_score': str(order.score),
                'comment': str(order.comment),
                'is_anonymous': str(order.is_anonymous),
                'order_id': str(order.order_id),
                'sku_id': sku.id
            })

        return render(request, 'goods_judge.html', {'uncomment_goods_list': skus})

    def post(self, request):
        # 接收数据
        query_dict = request.body.decode()
        data = json.loads(query_dict)
        order_id = data.get('order_id')
        sku_id = data.get('sku_id')
        comment = data.get('comment')
        score = data.get('score')
        is_anonymous = data.get('is_anonymous')
        # 校验数据

        if not all([order_id, sku_id, comment, score]):
            return http.HttpResponseForbidden('缺少必传参数')

        try:
            OrderGoods.objects.get(order_id=order_id, sku_id=sku_id)
        except OrderGoods.DoesNotExist:
            return http.HttpResponseForbidden('商品不存在')

        # 评论需要大于五个数字
        if len(comment) < 5:
            return http.JsonResponse('请填写大于5个数字的评论')

        OrderGoods.objects.filter(order_id=order_id,sku_id=sku_id).update(comment=comment,is_anonymous=is_anonymous, is_commented=True)

        # 查看整个订单状态
        comment_status = 0
        order = OrderInfo.objects.get(order_id=order_id,status=OrderInfo.ORDER_STATUS_ENUM['UNCOMMENT'])
        goods_list = OrderGoods.objects.filter(order_id=order_id)
        for goods in goods_list:
            if goods.is_commented:
                comment_status += 1

        # 如果所有订单商品均已评价，则将订单状态改为已完成
        if comment_status == len(goods_list):
            # order.update(status=OrderInfo.ORDER_STATUS_ENUM['FINISHED'])
            order.status = OrderInfo.ORDER_STATUS_ENUM['FINISHED']
            order.save()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})


class SKUCommentView(View):

    def get(self, request, sku_id):
        # 校验
        if not sku_id:
            return http.HttpResponseForbidden('缺少必传参数')

        comment_list = []
        goods_list = OrderGoods.objects.filter(sku_id=sku_id, is_commented=True)
        for goods in goods_list:
            buyer = '匿名用户' if goods.is_anonymous else goods.order.user.username
            comment_list.append({
                'buyer': buyer,
                'comment': goods.comment,
                'score': goods.score
            })

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'comment_list': comment_list})


class ForgetPassword(View):

    def get(self, request):
        return render(request, 'find_password.html')
