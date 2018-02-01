#-*- coding: UTF-8 -*-

import requests
import json

def do_spider():
    url='https://movie.douban.com/j/search_subjects'
    taglist=['热门','最新','经典','可播放','豆瓣高分','冷门佳片','华语','欧美','韩国','日本','动作','喜剧','爱情','科幻','悬疑','恐怖','成长']

    page_start=0
    tag_num=0
    while True:
        param={
            'type':'movie',
            'tag':taglist[tag_num],
            'sort':'rank',
            'page_limit':200,
            'page_start':page_start
        }
        r=requests.get(url,params=param)
        data=json.loads(r.text)
        
        subjects=data['subjects']

        if len(subjects)==0:
            tag_num+=1
            if tag_num==len(taglist):
                break
            page_start=0
        
        for i in range(len(subjects)):
            item=subjects[i]
            title=item['title']
            rate=item['rate']
            subjects[i]={
                'title':title,
                'rate':rate
            }

        ov=None

        with open('./rank.json', 'r') as f:
            obj=f.read()
            if obj:
                ov=json.loads(obj)
                ov['subjects'].extend(subjects)
            else:
                ov=data
            
            ov=json.dumps(ov)

        with open('./rank.json', 'w') as f:
            f.write(ov)

        page_start+=200
        print(page_start,tag_num)

do_spider()