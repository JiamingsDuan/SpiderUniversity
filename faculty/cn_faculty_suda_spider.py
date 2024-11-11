import json
import os
import random
import time
import requests
from urllib import request
from urllib.parse import urlencode
from tqdm import tqdm

save_path = 'json/'
img_path = 'img/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(save_path)
make_dir(img_path)
base_url = 'http://web.suda.edu.cn/_wp3services/generalQuery?'
payload = {
    'queryObj': 'teacherHome',
    'st': '0.6175719314806654',
}
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '928',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'JSESSIONID=D63E311499029EE6D14942B8EEA2C220; ipAddressName=',
    'Host': 'web.苏州suda.edu.cn',
    'Origin': 'http://web.suda.edu.cn',
    'Referer': 'http://web.suda.edu.cn/jsflcx/list.htm',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'X-Requested-With': 'XMLHttpRequest',
}
for page_index in range(49):
    form_data = {
        'pageIndex': page_index + 1,
        'rows': 20,
        'conditions': [{"field": "language", "value": "1", "judge": "="},
                       {"field": "published", "value": "1", "judge": "="}],
        'orders': [{"field": "letter", "type": "asc"}],
        'returnInfos': [{"field": "title", "name": "title"}, {"field": "cnUrl", "name": "cnUrl"},
                        {"field": "career", "name": "career"}, {"field": "headerPic", "name": "headerPic"},
                        {"field": "department", "name": "department"}, {"field": "post", "name": "post"},
                        {"field": "career", "name": "career"}, {"field": "visitCount", "name": "visitCount"},
                        {"field": "exField1", "name": "exField1"}],
        'articleType': 1,
        'level': 0,
        'pageEvent': 'doSearchByPage',
    }

    url = base_url + urlencode(payload)
    data = json.dumps(form_data)
    response = requests.post(url=url, headers=headers, data=urlencode(form_data), verify=False)
    faculty_list = response.json()['data']
    for faculty_dict in tqdm(faculty_list):
        name = faculty_dict['title']
        faculty_info_json = json.dumps(faculty_dict, indent=4, ensure_ascii=False)
        with open(save_path + name + '.json', 'w', encoding='utf-8') as f:
            f.write(faculty_info_json)
        img_url = 'http://web.suda.edu.cn' + faculty_dict['headerPic']
        try:
            img = request.urlretrieve(img_url, img_path + faculty_dict['title'] + '.jpg')
        except Exception as e:
            pass
        tds = random.randint(1, 10)
        time.sleep(tds / 10)
