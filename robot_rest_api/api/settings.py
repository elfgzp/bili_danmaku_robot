# -*- coding: utf-8 -*-
__author__ = 'gzp'

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from rest_framework.response import Response

from danmaku_robot.settings import Settings


class SettingsAPIView(APIView):
    http_method_names = ['get', 'put']
    permission_classes = (IsAuthenticated,)
    _settings = Settings()

    def get(self, request, *args, **kwargs):
        return Response(self._settings.values())

    def put(self, request, *args, **kwargs):
        for field in self._settings.fields():
            value = request.data.get(field)
            if value is not None:
                value = value if value is not False else ''
                setattr(self._settings, field, value)
        return Response(self._settings.values())
