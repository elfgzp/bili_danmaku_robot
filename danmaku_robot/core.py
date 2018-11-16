# -*- coding: utf-8 -*-
__author__ = 'gzp'

import time
import datetime
import asyncio
import logging

import django

django.setup()
from chatterbot.ext.django_chatterbot import settings
from chatterbot import ChatBot

from danmaku_robot.libs.pybililive.bililive import BiliLive
from danmaku_robot.libs.pybililive.definitions import Danmaku
from danmaku_robot.settings import Settings

_logger = logging.getLogger(__name__)


class Robot(object):
    def __init__(self, **kwargs):
        self.settings = Settings()
        self.client = None
        self.last_answer = ''
        self.robot = ChatBot(**settings.CHATTERBOT, read_only=True)
        self.cmd_func_dict = {
            'DANMU_MSG': self.handle_danmaku_msg
        }

        super(Robot, self).__init__(**kwargs)

    def run(self):
        while True:
            if not self.client or (self.client and self.settings_changed(self.client)):
                loop = asyncio.get_event_loop()

                self.client = BiliLive(
                    room_id=self.settings.room_id,
                    user_cookie=self.settings.cookie,
                    stop=self.stop_robot,
                    cmd_func_dict=self.cmd_func_dict,
                    loop=loop
                )
                asyncio.ensure_future(self.client.connect())
                loop.set_debug(True)
                try:
                    loop.run_forever()
                except Exception:
                    loop.close()
                self.client = None
            time.sleep(3)

    def settings_changed(self, robot):
        if robot.raw_room_id != self.settings.room_id:
            return True

        if robot.raw_cookie != self.settings.cookie:
            return True
        return False

    def stop_robot(self, robot):
        if self.settings_changed(robot):
            return True

    async def handle_danmaku_msg(self, live, message):
        danmaku = Danmaku(*message['info'])
        print('房间 {} {} {} 说: {}'.format(
            live.raw_room_id,
            datetime.datetime.fromtimestamp(danmaku.danmu_header[4]),
            danmaku.user_info[1],
            danmaku.content)
        )
        question_prefix = self.settings.question_prefix
        if danmaku.content.startswith(question_prefix if question_prefix else ''):
            await self.handle_question(danmaku.content)

    async def handle_question(self, question):
        if question != self.last_answer:
            answer = self.robot.get_response(question)
            if answer != question:
                self.last_answer = answer
                await self.client.send_danmu(answer.text)
