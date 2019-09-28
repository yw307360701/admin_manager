
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class MyPage(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "pagesize"
    page_size = 5
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        功能，自定义分页器响应的数据
        :param data: 分页到子集序列化到结果（字典）
        :return: 响应对象（构造响应数据）
        """
        return Response({
            "counts": self.page.paginator.count,
            "lists": data,
            "page": self.page.number,
            "pages": self.page.paginator.num_pages,
            "pagesize": self.page_size,
        })