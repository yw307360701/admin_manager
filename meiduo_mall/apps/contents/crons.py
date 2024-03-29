from .models import ContentCategory
from .utils import get_categories
import time, os
from django.shortcuts import render
from django.template import loader
from django.conf import settings


def generate_static_index_html():
    """
    生成静态的主页html文件
    """
    print('%s: generate_static_index_html' % time.ctime())

    # 广告内容
    contents = {}
    content_categories = ContentCategory.objects.all()
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

    # 渲染模板
    context = {
        'categories': get_categories(),  # 获取商品频道和分类
        'contents': contents
    }

    # response = render(None, 'index.html', context)
    # # 获取请求体中被渲染好的html字符串
    # content = response.content.decode()

    # 获取首页模板文件
    template = loader.get_template('index.html')
    # 渲染首页html字符串
    html_text = template.render(context)

    # 将首页html字符串写入到指定目录，命名'index.html'
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)
