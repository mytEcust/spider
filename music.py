#-*- coding: UTF-8 -*-

import json
from components import music, playlist, comment,clear,sort

api = None
with open('./config/default.json', 'r') as f:
    api = json.loads(f.read())

# playlist.get_all_playlist(api)
# music.get_all_music(api)
# comment.get_all_comment_num(api)
# clear.clear()
sort.sortComment()
print("done")

# 爬到金属(金属爬完)
