# 获取直播状态
# 如果没有直播，随机一段时间，再进行建东
# 如果在直播，则实例化历览器，记录当前时间，并开始下载直播
# 建立可视化网页，利用flask，进行直播管理，点击按钮获取直播状态，直接调用函数，每个页面用一个账号？每个账号负责不同的监控，保存加载的不同浏览信息。
# 按钮点击，点击后可以运行程序检测此时直播状态，点击开始检监测后执行程序，否则不执行，考虑加入高频直播时间段，而后在后台。
# 这样就需要对应数据库的读写了，记录每个账号的文件路径或者说对应文件名字，利用key
# 从检测一个
import datetime
import subprocess
import sys
import threading
import time

import flv_download
import getflv as gf
import common
import playwright_py



def format_total(flv_url,room_id, user_name,mongo_pool):
    event = threading.Event()
    p1 = threading.Thread(target=lambda: flv_download.download(flv_url, room_id))
    p2 = threading.Thread(
        target=lambda: playwright_py.load_login_getdanku(room_id, user_name, mongo_pool=mongo_pool, event=event))
    p2.setDaemon(True)
    p1.start()
    p2.start()
    p1.join()
    event.set()

def begin_total(room_id, user_name,mongo_pool):
    common_url = 'https://live.douyin.com/'
    room_url = common_url + room_id
    i = 0
    while True:
        # 获取直播状态
        state, info = gf.get_flvurl(room_url)
        if state:
            flv_url = info['flv_url']
            p = threading.Thread(target=lambda : format_total(flv_url,room_id, user_name,mongo_pool))
            p.start()
            p.join()
            # 检测到直播源没有输入后休息100s，防止出现不断地重启
            time.sleep(100)
        else:
            if i > 4:
                i = 0
                time.sleep(common.random_wiat_number() * 60)
            else:
                i += 1
                time.sleep(2)
                continue
