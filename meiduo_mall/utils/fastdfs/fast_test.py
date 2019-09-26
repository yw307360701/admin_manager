from fdfs_client.client import Fdfs_client


# 1.创建fastdfs客户端对象
client = Fdfs_client('./client.conf')

# 2.上传图片
ret = client.upload_by_filename('/home/python/Desktop/01.jpeg')


print(ret)