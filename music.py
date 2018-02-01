#-*- coding: UTF-8 -*-

import json
import requests
from bs4 import BeautifulSoup

def get_all_playlist():
    api=None
    with open('./public.json', 'r') as f:
        api=json.loads(f.read())
    headers = api['header']
    play_url = api['play_url']
    classify=api['classify']
    
    data=[]
    for fir in classify:
        print(fir)
        for sec in classify[fir]:
            print(sec)
            for i in range(1, 11):
                print(i)
                play_url=play_url.format(sec, i * 35)
                get_playlist(headers,play_url,data)

    return len(data)



def get_playlist(headers,play_url,data=[]):
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
        href = item.find('a', href_dom)['href']
        count= item.find('span', item_count_dom).text.replace('万', '0000')
        obj={
            'title':title,
            'href':href,
            'count':count
        }
        data.append(obj)


get_all_playlist()