# -*- coding: utf-8 -*-
__author__ = 'gzp'

from rest_framework import serializers
from chatterbot.ext.django_chatterbot.models import Response


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = (
            'id',
            'statement_id', 'statement',
            'response_id', 'response'
        )

    statement_id = serializers.PrimaryKeyRelatedField(
        source='statement',
        read_only=True
    )
    statement = serializers.CharField(source='statement.text', required=True)

    response_id = serializers.PrimaryKeyRelatedField(
        source='response',
        read_only=True
    )
    response = serializers.CharField(source='response.text', required=True)
