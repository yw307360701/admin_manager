from celery_tasks.sms.yuntongxun.sms import CCP
from celery_tasks.sms import constants
from celery_tasks.main import celery_app


# @celery_app.task()
# name自定义任务名字
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    # CCP().send_template_sms('接收短信手机号', ['短信验证码', '提示用户短信验证码多久过期单位分钟'], '模板id')
    CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_EXPIRE // 60], 1)
