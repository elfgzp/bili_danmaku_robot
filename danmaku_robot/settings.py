# -*- coding: utf-8 -*-
__author__ = 'gzp'

from danmaku_robot.models import RobotSettings


class Settings(object):
    _settings = dict([
        ('room_id', 'int'),
        ('cookie', 'str'),
        ('question_prefix', 'str'),
        ('confidence', 'float'),
        ('question_robot', 'bool'),
        ('robot_self_debug', 'bool'),
        ('merge_thank_gift', 'str'),
        ('thank_gift', 'bool')
    ])

    def __getattr__(self, item):
        if item not in self._settings.keys():
            raise AttributeError

        return RobotSettings.get_setting_value(item)

    def __setattr__(self, key, value):
        if key not in self._settings.keys():
            raise AttributeError

        RobotSettings.set_setting_value(key, value, default_type=self._settings[key])

    def values(self):
        return {
            key: getattr(self, key)
            for key in self._settings.keys()
        }

    def fields(self):
        return [key for key in self._settings.keys()]
