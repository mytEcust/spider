# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import json
from . import mongo

model = mongo.model()
model = model.db

def clear():
    musics = model['comments'].find()
    for music in musics:
        model['mm'].remove({'id':music['id']})
