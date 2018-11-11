# -*- coding: utf-8 -*-
__author__ = 'gzp'

from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'token', obtain_jwt_token, name='token')
]
