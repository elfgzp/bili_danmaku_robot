# -*- coding: utf-8 -*-
__author__ = 'gzp'

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

if __name__ == '__main__':
    deepThought = ChatBot("deepThought")
    deepThought.set_trainer(ListTrainer)

    response = deepThought.get_response("口红")
    print(response)
