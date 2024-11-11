import random
import requests
import json
import time
import math
import os
from tqdm import tqdm
from urllib import request, error

num = 2807
subject = "T"

base_url = 'https://c.wanfangdata.com.cn/Category/Magazine/search'
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'content-length': '306',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://c.wanfangdata.com.cn',
    'referer': 'https://c.wanfangdata.com.cn/periodical?class_code=' + subject,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55',
}

img_path = './wanfang/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(img_path)
for i in range(5, math.ceil(num / 100)):

    bit = random.randint(0, 5)
    digit = random.randint(0, 5)
    waiting = bit + digit / 10
    time.sleep(waiting)

    json_data = {
        "query": [],
        "start": 100 * i,
        "rows": 100,
        "sort_field": {"sort_field": "LastYear;HasFulltext;CoreScore"},
        "highlight_field": "",
        "pinyin_title": [],
        "class_code": subject,
        "core_periodical": [],
        "sponsor_region": [],
        "publishing_period": [],
        "publish_status": "",
        "return_fields": ['Id', 'Url', 'ISSN']
    }

    response = requests.post(url=base_url, data=json.dumps(json_data), headers=headers)
    contents = response.json()
    origin = 'https://www.wanfangdata.com.cn/images/PeriodicalImages/'
    for journal_info_dict in tqdm(contents['value']):
        journal_info_json = json.dumps(journal_info_dict, ensure_ascii=False, indent=4)
        journal_id = journal_info_dict['Id']
        ISSN = journal_info_dict['ISSN'].replace('\r', '').replace('\n', '').replace('/', '-')
        img_url = origin + str(journal_id) + '/' + str(journal_id) + '.jpg'
        try:
            img = request.urlretrieve(img_url, img_path + ISSN + '.jpg')
            # print(ISSN)
        except error.HTTPError as e:
            print(e, '暂无封面')
            pass
        time.sleep(0.1)
