import json
import random
import time
import os
import requests
import simplejson
from urllib import request, error
from urllib.parse import urlencode
from tqdm import tqdm

save_path = 'json/'
img_path = 'img/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(save_path)
make_dir(img_path)

base_url = 'http://faculty.cau.edu.cn/_wp3services/generalQuery?'
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '729',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'JSESSIONID=D8A9494C903175019281C6BAF4C8D2C8',
    'Host': 'faculty.中农cau.edu.cn',
    'Origin': 'http://faculty.cau.edu.cn',
    'Referer': 'http://faculty.cau.edu.cn/67/list.htm',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'X-Requested-With': 'XMLHttpRequest',
}

payload = {
    'queryObj': 'teacherHome',
}
for page_index in range(13):
    data = {
        'pageIndex': page_index + 1,
        'rows': 52,
        'conditions': [{"field": "language", "value": "1", "judge": "="},
                       {"field": "published", "value": "1", "judge": "="}],
        'orders': [{"field": "new", "type": "desc"}],
        'returnInfos': [{"field": "title", "name": "title"}, {"field": "cnUrl", "name": "cnUrl"},
                        {"field": "post", "name": "post"}, {"field": "headerPic", "name": "headerPic"},
                        {"field": "department", "name": "department"}, {"field": "exField1", "name": "exField1"}],
        'articleType': 1,
        'level': 0,
        'pageEvent': 'doSearchByPage',
    }

    url = base_url + urlencode(payload)
    response = requests.post(url=url, headers=headers, data=urlencode(data))
    faculty_list = response.json()['data']
    # print(response.status_code)
    for faculty_dict in tqdm(faculty_list):
        name = faculty_dict['title']
        faculty_info_json = json.dumps(faculty_dict, indent=4, ensure_ascii=False)
        with open(save_path + name + '.json', 'w', encoding='utf-8') as f:
            f.write(faculty_info_json)
        img_url = 'http://faculty.cau.edu.cn' + faculty_dict['headerPic']
        try:
            img = request.urlretrieve(img_url, img_path + faculty_dict['title'] + '.jpg')
        except Exception as e:
            pass
        tds = random.randint(1, 10)
        time.sleep(tds / 10)
