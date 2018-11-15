# -*- coding: utf-8 -*-
__author__ = 'gzp'

from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from robot_rest_api.api.settings import SettingsAPIView
from robot_rest_api.api.responses import ResponsesViewSet

urlpatterns = [
    url(r'token$', obtain_jwt_token, name='token'),
    url(r'settings$', SettingsAPIView.as_view(), name='settings'),
    url(r'responses$', ResponsesViewSet.as_view({'get': 'list', 'post': 'create'}), name='response_list'),
    url(r'responses/(?P<pk>[0-9]+)$', ResponsesViewSet.as_view({'get': 'retrieve'}), name='response_detail')
]
