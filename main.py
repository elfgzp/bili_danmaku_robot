# -*- coding: utf-8 -*-
__author__ = 'gzp'

from chat.graph import Database
from chat.qa import Robot

# userid 和 key 可在已有的3个测试用户中选或者自己添加

if __name__ == '__main__':
    # 初始化实例的时候若指定 userid 参数则会被导入 userid 对应用户，若不指定则导入通用用户
    # kb = Database(password='19900719')
    # kb.reset(filename='./tests_data/chat.xls')

    robot = Robot(password='19900719')
    result = robot.search(question='那我是男的还是女的', userid='A0001', key='A0001')
    answer = result['content']
    print(answer)
