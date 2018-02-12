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
    hasDone=[
      "朋克",
      "蓝调",
      "雷鬼",
      "世界音乐",
      "拉丁",
      "另类/独立",
      "New Age",
      "古风",
      "后摇",
      "Bossa Nova",
      "影视原声",
      "ACG",
      "校园",
      "游戏",
      "70后",
      "80后",
      "90后",
      "网络歌曲",
      "KTV",
      "经典",
      "翻唱",
      "吉他",
      "钢琴",
      "器乐",
      "儿童",
      "榜单",
      "00后",
      "怀旧",
      "清新",
      "浪漫",
      "性感",
      "伤感",
      "治愈",
      "放松",
      "孤独",
      "感动",
      "兴奋",
      "快乐",
      "安静",
      "思念",
      "清晨",
      "夜晚",
      "学习",
      "工作",
      "午休",
      "下午茶",
      "地铁",
      "驾车",
      "运动",
      "旅行",
      "散步",
      "酒吧"]
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