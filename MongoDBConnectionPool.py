import pymongo
import threading
from queue import Queue


# 创建连接池
class MongoDBConnectionPool:
    def __init__(self, max_pool_size, db_name,db_uri='mongodb://localhost:27017/'):
        self.max_pool_size = max_pool_size
        self.db_uri = db_uri
        self.db_name = db_name
        self._pools = {}
        self._lock = threading.Lock()

    def get_connection(self, collection_name):
        client = pymongo.MongoClient(self.db_uri)
        print(client[self.db_name][collection_name]
)
        return client[self.db_name][collection_name]

