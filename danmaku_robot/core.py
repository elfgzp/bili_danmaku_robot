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
from danmaku_robot.definitions import GiftModel, GiftQueue
from danmaku_robot.settings import Settings

_logger = logging.getLogger(__name__)


class Robot(object):
    def __init__(self, **kwargs):
        self.settings = Settings()
        self.client = None
        self.gift_queue = GiftQueue()
        self._gift_consumer = None
        self.robot = ChatBot(**settings.CHATTERBOT, read_only=True)
        self.cmd_func_dict = {
            'DANMU_MSG': self.handle_danmaku_msg,
            'SEND_GIFT': self.handle_gift
        }

        super(Robot, self).__init__(**kwargs)

    def run(self):
        while True:
            if not self.client or (self.client and self.settings_changed(self.client)):
                loop = asyncio.get_event_loop()
                self._gift_consumer = asyncio.ensure_future(self.consume_gift())
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
        message['name_color'] = message.get('name_color', '')
        danmaku = Danmaku(*message['info'])
        print('房间 {} {} {} 说: {}'.format(
            live.raw_room_id,
            datetime.datetime.fromtimestamp(danmaku.danmu_header[4]),
            danmaku.user_info[1],
            danmaku.content)
        )
        question_prefix = self.settings.question_prefix
        if self.settings.robot_self_debug or self.client._user_name and self.client._user_name != danmaku.user_info[1]:
            if self.settings.question_robot and danmaku.content.startswith(
                    question_prefix if question_prefix else ''):
                await self.handle_question(danmaku.content)

    async def handle_question(self, question):
        answer = self.robot.get_response(question)
        print("Q: %s A: %s C: %s" % (question, answer, answer.confidence))
        if answer != question and answer.confidence >= self.settings.confidence:
            await self.client.send_danmu(answer.text)

    async def handle_gift(self, live, message):
        user_name = message['data']['uname']
        uid = message['data']['uid']
        gift_id = message['data']['giftId']
        gift_name = message['data']['giftName']
        num = message['data']['num']
        print('{} 送出了 {}x{}'.format(user_name, gift_name, num))
        if self.client._user_name:
            if str(gift_id) in self.settings.merge_thank_gift.split(','):
                gift = GiftModel(
                    publisher_uid=uid,
                    publisher_name=user_name,
                    gift_id=gift_id,
                    gift_name=gift_name
                )
                if self.settings.thank_gift:
                    self.put_gift(gift)
            else:
                await self.client.send_danmu('感谢{}送出的{}x{}'.format(user_name, gift_name, num))

    async def consume_gift(self):
        while True:
            try:

                current_gift_count = len(self.gift_queue)
                thanks = '感谢{}赠送的礼物~'
                publisher_name_list = []
                publisher_uid_set = set()
                if current_gift_count <= 3:
                    sleep_time = 40
                elif current_gift_count <= 8:
                    sleep_time = 30
                elif current_gift_count <= 10:
                    sleep_time = 20
                else:
                    sleep_time = 10

                while current_gift_count > 0:
                    gift = self.get_gift()

                    # compress publisher name
                    while gift:
                        if gift.publisher_uid not in publisher_uid_set:
                            publisher_name_list.append(gift.publisher_name)
                            publisher_uid_set.add(gift.publisher_uid)

                        if len(thanks.format('、'.join(publisher_name_list))) >= 30:
                            self.put_gift(gift)
                            publisher_name_list.pop()
                            thanks = thanks.format('、'.join(publisher_name_list))
                            print(thanks)
                            if self.settings.thank_gift:
                                await self.client.send_danmu(thanks)
                            thanks = '感谢{}赠送的礼物~'
                            publisher_name_list = []
                            await asyncio.sleep(2)
                            break
                        gift = self.get_gift()
                        current_gift_count -= 1
                    else:
                        if publisher_name_list:
                            thanks = thanks.format('、'.join(publisher_name_list))
                            print(thanks)
                            if self.settings.thank_gift:
                                await self.client.send_danmu(thanks)
                            thanks = '感谢{}赠送的礼物~'
                            publisher_name_list = []

                await asyncio.sleep(sleep_time)

            except Exception as e:
                _logger.exception(e)

    def put_gift(self, gift):
        self.gift_queue.enqueue(gift)

    def get_gift(self):
        return self.gift_queue.dequeue()
