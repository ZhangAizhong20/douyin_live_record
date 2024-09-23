import asyncio
import datetime
import gzip
import sched
import sys
import threading
import uuid
import time
import os
from google.protobuf.json_format import MessageToDict
from playwright.sync_api import sync_playwright as playwright

import common
import message_pb2
from pymongo import MongoClient
from MongoDBConnectionPool import MongoDBConnectionPool


# args = sys.argv[1:]
# room_id = args[0]
# user = args[1]
#
# url = 'https://live.douyin.com/'
#     url = url + room_id
# 链接数据库，创建对应collectionmas
def init_database(room_id, mongo_pool: MongoDBConnectionPool):
    client = MongoClient("mongodb://localhost:27017")
    # 指定数据库和集合名称
    db_name = "douyin_danmu_test"
    collection_name = str(room_id) + '-' + common.get_current_time()

    # 获取数据库对象
    db = client[db_name]
    # 检查集合是否存在
    if collection_name in db.list_collection_names():
        print("Collection already exists.")
    else:
        # 创建集合
        db.create_collection(collection_name)
    collection = db[collection_name]
    return collection


def wss(websocket):
    if 'douyin.com/webcast/im/push/v2/?' in websocket.url:
        websocket.on('framereceived', wss_onmessage)

def wss_onmessage(framereceived):

    o = message_pb2.PushFrame()
    o.ParseFromString(framereceived)
    payload = o.palyload
    for t in o.headersList:
        if t.key == 'compress_type' and t.value == "gzip":
            payload = gzip.decompress(o.palyload)
            break
    r = message_pb2.Response()
    r.ParseFromString(payload)
    e = r
    messagelist = e.messages
    for t in messagelist:
        o = t.payload
        message_ = ''
        if t.method == "WebcastGiftMessage":
            message_ = message_pb2.GiftMessage()
            message_.ParseFromString(o)
        elif t.method == "WebcastChatMessage":
            message_ = message_pb2.ChatMessage()
            message_.ParseFromString(o)
        elif t.method == "WebcastMemberMessage":
            message_ = message_pb2.MemberMessage()
            message_.ParseFromString(o)
        elif t.method == "WebcastSocialMessage":
            message_ = message_pb2.SocialMessage()
            message_.ParseFromString(o)
        if message_:
            obj1 = MessageToDict(message_, preserving_proto_field_name=True)
            obj1['record_time'] = datetime.datetime.now()
            print(obj1)



def click_page(page):
    print('begin_click')
    try:
        screen_size = page.evaluate('() => ({ width: window.innerWidth, height: window.innerHeight })')
        # 计算屏幕中心点的坐标
        center_x = screen_size['width'] // 2
        center_y = screen_size['height'] // 2
        # 在中心点进行单击
        page.mouse.click(center_x + common.random_wiat_number() * 0.1, center_y, click_count=2)
        print('success')
    except: print('failed_click')


def load_login_getdanku(room_id, user, mongo_pool: MongoDBConnectionPool,event:threading.Event):
    collection_name = str(room_id) + '-' + common.get_current_time()
    connection = mongo_pool.get_connection(collection_name)

    def wss(websocket):
        if 'douyin.com/webcast/im/push/v2/?' in websocket.url:
            websocket.on('framereceived', wss_onmessage)

    def wss_onmessage(framereceived):
        o = message_pb2.PushFrame()
        o.ParseFromString(framereceived)
        payload = o.palyload
        for t in o.headersList:
            if t.key == 'compress_type' and t.value == "gzip":
                payload = gzip.decompress(o.palyload)
                break
        r = message_pb2.Response()
        r.ParseFromString(payload)
        e = r
        messagelist = e.messages
        i = 0
        insert_list = []
        for t in messagelist:
            o = t.payload
            message_ = ''
            if t.method == "WebcastGiftMessage":
                message_ = message_pb2.GiftMessage()
                message_.ParseFromString(o)
            elif t.method == "WebcastChatMessage":
                message_ = message_pb2.ChatMessage()
                message_.ParseFromString(o)
            elif t.method == "WebcastMemberMessage":
                message_ = message_pb2.MemberMessage()
                message_.ParseFromString(o)
            elif t.method == "WebcastSocialMessage":
                message_ = message_pb2.SocialMessage()
                message_.ParseFromString(o)
            if message_:
                obj1 = MessageToDict(message_, preserving_proto_field_name=True)
                obj1['record_time'] = datetime.datetime.now()
                # print(obj1)
                insert_list.append(obj1)
                # print('here')
        if len(insert_list) > 0:
            connection.insert_many(insert_list)
    url = 'https://live.douyin.com/'
    url = url + room_id

    with playwright() as pw:
        browser =  pw.chromium.launch(headless=False)
        user_file_name = str(user) + '.json'
        user_file = os.path.join('user_file', user_file_name)
        context = browser.new_context(storage_state=user_file)
        page = context.new_page()
        page.on("websocket", wss)
        page.goto(url, timeout=0)
        current_time = datetime.datetime.now()
        time_deta = common.random_wiat_number()*60
        while not event.is_set():
            page.wait_for_timeout(2)
            if datetime.datetime.now() > current_time + datetime.timedelta(seconds=time_deta):
                try:
                    click_page(page)
                except:print("failed")
                current_time = datetime.datetime.now()
                time_deta = common.random_wiat_number()*60
        page.close()



# def set_login(name):
#     browser = pw.firefox.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto(url, timeout=0)
#     time.sleep(50)
#     path = str(name) + '.json
#     context.storage_state(path=path)


# load_login_getdanku(url, user)

# 创建浏览器
if __name__ == '__main__':
    with playwright() as pw:
        room_id = '80017709309'
        common_url = 'https://live.douyin.com/'
        room_url = common_url + room_id
        # 创建一个webkit,
        # headless=True后台执行抓包
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(storage_state='user1.json')
        page = context.new_page()
        page.on("websocket", wss)
        page.goto(room_url, timeout=0)
        while True:
            page.wait_for_timeout(1)
