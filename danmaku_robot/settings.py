# -*- coding: utf-8 -*-
__author__ = 'gzp'

from danmaku_robot.models import RobotSettings


class Settings(object):
    _settings = dict([
        ('room_id', 'int'),
        ('cookie', 'str'),
        ('question_prefix', 'str')
    ])

    def __getattr__(self, item):
        if item not in self._settings.keys():
            raise AttributeError

        return RobotSettings.get_setting_value(item)

    def __setattr__(self, key, value):
        if key not in self._settings.keys():
            raise AttributeError

        RobotSettings.set_setting_value(key, value, default_type=self._settings[key])
