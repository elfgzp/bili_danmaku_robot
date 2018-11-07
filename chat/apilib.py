# -*- coding: utf-8 -*-

"""Api lib for simple life."""
import os
import json
import requests
import time
import uuid
from urllib.request import urlopen

mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]


def get_location_by_ip(city="上海市"):
    """根据IP获取当前地址
    """
    url = "http://api.map.baidu.com/location/ip"
    data = {
        "ak": "wllxHD5CmWv8qX6CN2lyY73a",
        "coor": "bd09ll"
    }
    try:
        result = requests.post(url, data, timeout=20).text
        location = json.loads(result)["content"]["address"]
        print("当前所在城市：", location)
    except:
        location = city
        print("采用默认城市：", location)
    return location
