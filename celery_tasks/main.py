# celery 启动文件
from celery import Celery
import os

# 让celery在启动时提前加载django配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")

# 1.创建celery客户端对象
celery_app = Celery('meiduo')
# 2.加载celery配置，指定celery生产的任务放在哪里
celery_app.config_from_object('celery_tasks.config')
# 3.注册celery可以生存什么任务(后面的tasks写死，文件必须以tasks命名）
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])