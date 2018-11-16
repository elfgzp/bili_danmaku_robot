# -*- coding: utf-8 -*-
__author__ = 'gzp'

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_extensions.mixins import NestedViewSetMixin

from chatterbot.ext.django_chatterbot.models import Response as ResponseModel
from chatterbot.trainers import ListTrainer

from chatterbot.ext.django_chatterbot import settings
from chatterbot import ChatBot

from robot_rest_api.serializers.response import ResponseSerializer
from robot_rest_api.paginations import APIPagination


class ResponsesViewSet(NestedViewSetMixin, ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ResponseModel.objects.all()
    serializer_class = ResponseSerializer
    pagination_class = APIPagination
    search_fields = ('response__text', 'statement__text')
    robot = ChatBot(**settings.CHATTERBOT, read_only=True)
    robot.set_trainer(ListTrainer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.perform_create(serializer)
        serializer = self.get_serializer(instance)

        headers = self.get_success_headers(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        self.queryset.filter(statement__text=serializer.initial_data['statement']).delete()
        self.robot.train([
            serializer.initial_data['statement'],
            serializer.initial_data['response']
        ])
        return self.queryset.filter(statement__text=serializer.initial_data['statement']).first()
