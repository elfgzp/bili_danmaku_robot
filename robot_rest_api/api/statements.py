# -*- coding: utf-8 -*-
__author__ = 'gzp'

from rest_framework.viewsets import ReadOnlyModelViewSet

from rest_framework.permissions import IsAuthenticated

from chatterbot.ext.django_chatterbot.models import Statement

from robot_rest_api.serializers.statement import StatementSerializer
from robot_rest_api.paginations import APIPagination


class StatementsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Statement.objects.all()
    serializer_class = StatementSerializer
    pagination_class = APIPagination
