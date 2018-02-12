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