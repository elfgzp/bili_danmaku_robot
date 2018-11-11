# -*- coding: utf-8 -*-
__author__ = 'gzp'


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'uuid': user.pk,
        'name': user.username,
        'token': token
    }
