from django.core.files.storage import Storage
from django.conf import settings


class FastDFSStorage(Storage):
    """自定义文件存储类"""

    def _open(self, name, mode='rb'):
        """
        当要打开某个文件时就会自动调用此方法
        :param name: 要打开的文件名
        :param mode: 打开文件模式 二进制读取
        :return: 打开的文件对象
        """
        pass

    def _save(self, name, content):
        """
        当上传文件时,就会自动调用此方法
        :param name: 文件名
        :param content: 被读取出来的文件二进制数据
        :return: file_id
        """
        pass


    def url(self, name):
        """
        当调用image字典的url属性时就会自动调用此方法获取要下载图片的绝对路径
        :param name: file_id
        :return: 图片绝对路径: http://192.168.103.210:8888/ + file_id
        """
        # return 'http://192.168.233.131:8888/' + name
        return settings.FDFS_BASE_URL + name
