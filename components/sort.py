# -*- coding: utf-8 -*-

from . import mongo
from pymongo import MongoClient, DESCENDING

model = mongo.model()
model = model.db

def sortComment():
    musics=model['comments'].find({}).sort("totalCount",DESCENDING).limit(100)
    for music in musics:
        item=model['musics'].find({'id':music['id']})
        for i in item:
            print(i['name'])