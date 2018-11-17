# -*- coding: utf-8 -*-
__author__ = 'gzp'

import django
import multiprocessing

from django.contrib.staticfiles.management.commands.runserver import Command as RunserverCommand

from danmaku_robot.core import Robot

ROBOT_PROCESS = None


class Command(RunserverCommand):
    def run(self, **options):
        options['use_reloader'] = False
        django.setup()
        self.run_robot()
        super(Command, self).run(**options)

    def run_robot(self):
        robot_process = multiprocessing.Process(target=Robot().run, args=())
        robot_process.daemon = True
        robot_process.start()
