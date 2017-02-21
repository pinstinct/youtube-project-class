"""
1. .conf 폴더의 settings_local.json을 읽어서
2. 해당 내용을 json.loads()를 이용해 str -> dict 형태로 변환
3. requests 라이브러리를 이용(pip install reqest), GET요청으로 테이터를 받아온 후
4. 해당 내용을 다시 json.loads()를 이용해 파이썬 객체로 변환
5. 이후 내부에 있는 검색결과를 적절히 루프하여 print 해주기
"""
import json
import os

import requests

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_DIR = os.path.join(ROOT_DIR, '.conf')

content = json.loads(open(os.path.join(CONF_DIR, 'settings_local.json')).read())

payload = {
    'part': 'snippet',
    'q': 'grizemanmm',
    'maxResults': 50,
    'key': content['youtube']['API_KEY'],
}

r = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
raw_dic = r.json()
max_result = raw_dic['pageInfo']['resultsPerPage']

for i in range(max_result):
    title = raw_dic['items'][i]['snippet']['title']
    print('title: {}'.format(title))
