# -*- coding: utf-8 -*-
__author__ = 'gzp'

from chatterbot.chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

from chatterbot.ext.django_chatterbot import settings

from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.response import Response


class LiveClient(APIView):
    chatterbot = ChatBot(**settings.CHATTERBOT)

    def get(self, request, *args, **kwargs):
        action = request.query_params.get('action')
        q = request.query_params.get('q')
        a = request.query_params.get('a')

        if not action:
            raise exceptions.ValidationError()

        if action == 't':
            self.chatterbot.set_trainer(ListTrainer)
            self.chatterbot.train([q, a])
            return Response({'q': a})

        if action == 'a':
            a = self.chatterbot.get_response(q)
            return Response({'q': str(a)})
