# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import json
from . import mongo

model = mongo.model()
model.create_index('musics', 'id')
model = model.db

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_music(headers, playlist_url):
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, playlist_url)
        result = json.loads(result)
        for item in result['result']['tracks']:
            name = item['name']
            artists = item['artists'][0]['name']
            obj = {
                'name': name,
                'artists': artists,
                'id': id
            }
            try:
                print('in')
                model['musics'].insert(obj)
            except Exception as e:
                print('not in')


def get_all_music(api):
    headers = api['header']
    music_url = api['music_url']
    playlists = model['playlist'].find()
    promise = []
    loop = asyncio.get_event_loop()
    for playlist in playlists:
        if playlist['classify'] in hasDone:
            if len(promise)==10:
                
                # 执行coroutine
                loop.run_until_complete(asyncio.wait(promise))
                
                promise=[]
            else:
                promise.append(get_music(headers, music_url+playlist['id']))
    loop.close()