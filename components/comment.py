# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import json
from . import mongo

model = mongo.model()
model.create_index('comments', 'id')
model = model.db


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_comment_num(headers, comment_url, music_id):
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, comment_url)
        result = json.loads(result)
        totalCount = result['totalCount']
        
        obj = {
            'totalCount': int(totalCount),
            'id': music_id
        }
        try:
            model['comments'].insert(obj)
            print('in')
        except Exception as e:
            print('not in')


def get_all_comment_num(api):
    headers = api['header']
    comment_url = api['comment_url']
    musics = model['musics'].find()
    comments=model['comments'].find({},{"id":1})
    loop = asyncio.get_event_loop()
    # print(musics[34451:37750])
    for music in musics[37750:]:
        # 执行coroutine
        loop.run_until_complete(get_comment_num(headers, comment_url.format(music['id']), music['id']))
    loop.close()
