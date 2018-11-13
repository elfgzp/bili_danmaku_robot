# -*- coding: utf-8 -*-
__author__ = 'gzp'

import time
import asyncio

from danmaku_robot.libs.pybililive.bililive import BiliLive
from danmaku_robot.settings import Settings


def stop_robot(robot):
    setting = Settings()
    if robot.raw_room_id != setting.room_id:
        return True

    if robot.user_cookie != setting.cookie:
        return True


class Robot(object):
    def __init__(self, **kwargs):
        self.settings = Settings()
        self.client = None

        super(Robot, self).__init__(**kwargs)

    def run(self):
        while True:
            if self.settings.room_id:
                loop = asyncio.get_event_loop()

                self.client = BiliLive(
                    room_id=self.settings.room_id,
                    user_cookie=self.settings.cookie,
                    stop=stop_robot,
                    loop=loop
                )
                asyncio.ensure_future(self.client.connect())
                loop.set_debug(True)
                try:
                    loop.run_forever()
                except Exception:
                    loop.close()
            time.sleep(3)
