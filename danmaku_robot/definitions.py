# -*- coding: utf-8 -*-
__author__ = 'gzp'


class GiftModel(object):
    def __init__(self, publisher_uid, publisher_name, gift_id, gift_name):
        self.publisher_uid = publisher_uid
        self.publisher_name = publisher_name
        self.gift_id = gift_id
        self.gift_name = gift_name

    def __str__(self):
        return '感谢{publisher_name}赠送的礼物~'.format(
            publisher_name=self.publisher_name, gift_name=self.gift_name
        )

    def to_string(self):
        return self.__str__()


class GiftQueue(object):
    def __init__(self):
        self._queue = []
        self._queue_hash = set()

    def __len__(self):
        return len(self._queue)

    def enqueue(self, gift):
        if isinstance(gift, GiftModel):
            if gift.publisher_uid and gift.publisher_uid not in self._queue_hash:
                self._queue.append(gift)
                self._queue_hash.add(gift.publisher_uid)
                return True
        return False

    def dequeue(self):
        if self._queue:
            gift = self._queue.pop(0)
            self._queue_hash.remove(gift.publisher_uid)
            return gift
        return None
