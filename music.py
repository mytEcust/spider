#-*- coding: UTF-8 -*-

import json
import requests
import urllib
from bs4 import BeautifulSoup
from pymongo import MongoClient

settings = {
    "ip":'localhost',   #ip
    "port":27017,           #端口
    "db_name" : "spider",    #数据库名字
    # "set_name" : "playlist"   #集合名字
}

class MyMongoDB(object):
    def __init__(self):
        try:
            self.conn = MongoClient(settings["ip"], settings["port"])
        except Exception as e:
            print(e)
        self.db = self.conn[settings["db_name"]]
        # self._set = self.db[settings["set_name"]]

    def insert(self,table,dic):
        _table = self.db[table]
        _table.insert(dic)

    def update(self,table,dic,newdic):
        _table = self.db[table]
        _table.update(dic,newdic)

    def delete(self,table,dic):
        _table = self.db[table]
        _table.remove(dic)

    def find(self,table,dic):
        _table = self.db[table]
        data = _table.find(dic)
        return data

    def count(self,table,dic):
        _table = self.db[table]
        return _table.count(dic)

mongo = MyMongoDB()
api=None
with open('./public.json', 'r') as f:
    api=json.loads(f.read())


def get_all_playlist(api):
    headers = api['header']
    play_url = api['play_url']
    classify=api['classify']

    for fir in classify:
        print(fir)
        for sec in classify[fir]:
            print(sec)
            sec=urllib.parse.quote(sec)
            for i in range(1, 11):
                _play_url=play_url.format(sec, i*35)
                print(_play_url)
                get_playlist(headers,_play_url)



def get_playlist(headers,play_url):
    s = requests.session()
    dom = BeautifulSoup(s.get(play_url, headers=headers).content, "html.parser")
    # 歌单列表外壳
    list_box_dom = {'class': 'm-cvrlst f-cb'}
    # 歌单外壳
    item_box_dom = {'class': 'u-cover u-cover-1'}
    # 歌单href
    href_dom = {'class': 'msk'}
    # 播放次数
    item_count_dom = {'class': 'nb'}

    list_box = dom.find('ul', list_box_dom)
    for item in list_box.find_all('div',item_box_dom):
        title=item.find('a', href_dom)['title']
        id = item.find('a', href_dom)['href'].replace("/playlist?id=", "")
        count= item.find('span', item_count_dom).text.replace('万', '0000')
        obj={
            'title':title,
            'id':id,
            'count':count
        }
        # print(title,id)
        
        count=mongo.count('playlist',{'id':id})
        # print(count)
        if(count==0):
            mongo.insert('playlist',obj)

def get_music(headers,playlist_url):
    s = requests.session()
    result=s.get(playlist_url, headers=headers)
    result=json.loads(result.text)

    for item in result['result']['tracks']:
        name=item['name']
        artists=item['artists'][0]['name']
        id=item['id']
        obj={
            'name':name,
            'artists':artists,
            'id':id
        }

        count=mongo.count('musics',{'id':id})
        if(count==0):
            mongo.insert('musics',obj)

def get_all_music(api):
    headers = api['header']
    music_url = api['music_url']
    playlists=mongo.find('playlist',{})
    for playlist in playlists:
        print(playlist['title'])
        get_music(headers,music_url+playlist['id'])

get_all_playlist(api)
get_all_music(api)
print("done")

# 爬到金属(金属爬完)