import gzip
import time
import os
import uuid

from google.protobuf.json_format import MessageToDict
from playwright.sync_api import sync_playwright as playwright
import message_pb2
url = 'https://live.douyin.com/80017709309'


def wss(websocket):
    print(websocket.url)
    if 'douyin.com/webcast/im/push/v2/?' in websocket.url:
        websocket.on('framereceived',wss_onmessage)

def wss_onmessage(framereceived):
    print(type(framereceived))
    print(framereceived)
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
            print(obj1)



# 创建浏览器
with playwright() as pw:
    # 创建一个webkit,
    # headless=True后台执行抓包
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # page.on("websocket", wss)
    page.goto(url, timeout=0)
    time.sleep(50)
    context.storage_state(path='user1.json')

