# -*- coding: utf-8 -*-
__author__ = 'gzp'

from rest_framework import serializers
from chatterbot.ext.django_chatterbot.models import Statement


class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = (
            'id', 'text', 'extra_data'
        )

