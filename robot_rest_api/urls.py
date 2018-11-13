# -*- coding: utf-8 -*-
__author__ = 'gzp'

from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from robot_rest_api.api.live_client import LiveClient

urlpatterns = [
    url(r'token', obtain_jwt_token, name='token'),
    url(r'live_client', LiveClient.as_view(), name='live_client')
]
