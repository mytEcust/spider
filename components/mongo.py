# -*- coding: utf-8 -*-

from pymongo import MongoClient, ASCENDING

settings = {
    "ip": 'localhost',  # ip
    "port": 27017,  # 端口
    "db_name": "spider",  # 数据库名字
}

class MongoDB(object):
    def __init__(self):
        try:
            self.conn = MongoClient(settings["ip"], settings["port"])
        except Exception as e:
            print(e)
        self.db = self.conn[settings["db_name"]]

    def create_index(self, table, name):
        self.db[table].create_index([(name, ASCENDING)], unique=True)

client = MongoDB()
def model():
    return client
