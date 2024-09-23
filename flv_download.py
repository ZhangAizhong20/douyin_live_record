import datetime
import re
import os
import time

import requests
import sys

import common
import common as com
import Settings

def download(url, room_id):
    print("开始下载..." + url)
    size = 0
    response = requests.get(url, stream=True)
    file_name = room_id+'-' + com.get_current_time() + '.flv'
    file_path = os.path.join(Settings.FILE_FOLDER, file_name)
    with open(file_path, 'wb') as file:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            size += len(data)
            file.flush()
            sys.stdout.write('\r[下载进度]:%.2fMB' % float(size / 1024 / 1024))
            sys.stdout.flush()
    file.close()


