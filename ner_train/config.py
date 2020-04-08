# import sqlite3
import os
import pymongo
# from albert_pytorch import classify

# from  tkitMarker import  *

#这里定义mongo数据
client = pymongo.MongoClient("localhost", 27017)
DB = client.gpt2Write
print(DB.name)
# DB.my_collection
# Collection(Database(MongoClient('localhost', 27017), u'test'), u'my_collection')
# print(DB.my_collection.insert_one({"x": 10}).inserted_id)
