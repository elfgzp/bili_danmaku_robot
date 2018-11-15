# -*- coding: utf-8 -*-
__author__ = 'gzp'

from rest_framework.pagination import PageNumberPagination


class APIPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 40
