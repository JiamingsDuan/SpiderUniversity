from urllib import request, error
import requests
import json
import simplejson
import math
from pymongo import MongoClient
from tqdm import tqdm
from urllib.parse import urlencode

base_dir = 'images_university/'
base_url = 'https://api.eol.cn/gkcx/api/?'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://gkcx.eol.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29 '
}

for page in range(1, 142):
    json_data = {
        "access_token": "",
        "admissions": "",
        "central": "",
        "department": "",
        "dual_class": "",
        "f211": "",
        "f985": "",
        "is_doublehigh": "",
        "is_dual_class": "",
        "keyword": "",
        "nature": "",
        "page": page,
        "province_id": "",
        "ranktype": "",
        "request_type": 1,
        "school_type": "",
        "size": 20,
        "sort": "",
        "top_school_id": "",
        "type": "",
        "uri": "apidata/api/gk/school/lists"
    }
    urls = base_url + urlencode(json_data)
    html = requests.post(url=urls, headers=headers)
    html_str = html.content.decode('utf-8')
    contents = simplejson.loads(html_str)
    # print(contents)
    # print(type(contents))
    for item in contents['data']['item']:
        code = item['school_id']
        name = item['name']
        print(name, code)
        # university_url = 'https://static-data.eol.cn/www/2.0/school/' + str(code) + '/info.json'
        img_url = 'https://static-data.eol.cn/upload/logo/' + str(code) + '.jpg'
        try:
            img = request.urlretrieve(img_url, base_dir + name.replace('/', '_') + '.jpg')
            # print(journal_info['Title'][0] + '-> save success')
        except error.HTTPError as e:
            # print(e.code)
            pass

