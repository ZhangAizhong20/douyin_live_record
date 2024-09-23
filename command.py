import functools
import random
import subprocess
import time
from multiprocessing import Process

import pymongo

import Settings

# process_id = '80017709309'
# process_id_list = ['242374537996','332751307178','80017709309','168465302284','169353329957']
# args = [str(process_id), 'user1']
# command = ['python', 'F:\github\\douyin_alike_dan\\total.py'] + args
# # 启动新的子进程
# process = subprocess.Popen(command)
# output, _ = process.communicate()
#
# # 输出子进程的输出结果
# print(output.decode())
import total
import threading
import multiprocessing
from MongoDBConnectionPool import MongoDBConnectionPool




if __name__ == '__main__':
    processes = []
    process_id_list = Settings.ROOM_ID_LIST

    # process_id_list = ['166902759']

    user_name = Settings.USER_NAME
    mongo_pool = MongoDBConnectionPool(max_pool_size=50, db_uri='mongodb://localhost:27017/', db_name=Settings.DATABASE_NAME)
    # MongoDBclient = pymongo.MongoClient('mongodb://localhost:27017/')
    for process_id in process_id_list:
        target_func = functools.partial(total.begin_total, process_id,random.choice(user_name),mongo_pool)
        processes.append(threading.Thread(target=target_func))
        # processes.append(multiprocessing.Process(target=target_func))

    for t in processes:
        t.start()
    for t in processes:
        t.join()

    print("所有子进程执行完成。")