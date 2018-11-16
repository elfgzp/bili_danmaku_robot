# -*- coding: utf-8 -*-
__author__ = 'gzp'

from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from robot_rest_api.api.settings import SettingsAPIView
from robot_rest_api.api.responses import ResponsesViewSet
from robot_rest_api.api.statements import StatementsViewSet

urlpatterns = [
    path('token', obtain_jwt_token, name='token'),
    path('settings', SettingsAPIView.as_view(), name='settings'),
    path('responses', ResponsesViewSet.as_view({'get': 'list', 'post': 'create'}), name='response_list'),
    path('responses/<int:pk>', ResponsesViewSet.as_view(
        {'get': 'retrieve', 'delete': 'destroy'}),
         name='response_detail'),
    path('statements/<int:parent_lookup_statement__pk>/responses',
         ResponsesViewSet.as_view({'get': 'list'}),
         name='statement_response_list'),
    path('statements/<int:parent_lookup_statement__pk>/responses/<int:pk>',
         ResponsesViewSet.as_view({'get': 'retrieve'}),
         name='statement_response_detail'),

    path('statements', StatementsViewSet.as_view({'get': 'list'}), name='statement_list'),
    path('statements/<int:pk>', StatementsViewSet.as_view({'get': 'retrieve'}), name='statement_detail'),
]
