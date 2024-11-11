import json
import os
import random
import time
import requests
from urllib.parse import urlencode
from urllib import request, error
from tqdm import tqdm

save_path = 'json/'
img_path = 'img/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(save_path)
make_dir(img_path)

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '735',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'JSESSIONID=A89B4037E156D438CB016DEBABEB0BEF',
    'Host': 'faculty.jnu.edu.cn',
    'Origin': 'https://faculty.jnu.edu.cn',
    'Referer': 'https://faculty.jnu.edu.cn/1212/list.htm',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'X-Requested-With': 'XMLHttpRequest',
}

payload = {
    'queryObj': 'teacherHome'
}
for page_index in range(22):
    form_data = {
        'pageIndex': page_index + 1,
        'rows': 52,
        'conditions': [{"field": "language", "value": "1", "judge": "="},
                       {"field": "published", "value": "1", "judge": "="}],
        'orders': [{"field": "letter", "type": "asc"}],
        'returnInfos': [{"field": "title", "name": "title"},
                        {"field": "cnUrl", "name": "cnUrl"},
                        {"field": "career", "name": "career"},
                        {"field": "headerPic", "name": "headerPic"},
                        {"field": "department", "name": "department"},
                        {"field": "exField1", "name": "exField1"}],
        'articleType': 1,
        'level': 0,
        'pageEvent': 'doSearchByPage',
    }

    base_url = 'https://faculty.jnu.edu.cn/_wp3services/generalQuery?'
    url = base_url + urlencode(payload)
    response = requests.post(url=url, data=urlencode(form_data), headers=headers)
    contents = response.json()['data']
    for faculty_index in tqdm(range(len(contents))):
        faculty_dict = contents[faculty_index]
        name = faculty_dict['title'].replace(' ', '')
        faculty_info_json = json.dumps(faculty_dict, indent=4, ensure_ascii=False)
        with open(save_path + name + '.json', 'w', encoding='utf-8') as fo:
            fo.write(faculty_info_json)
            fo.close()
        img_url = 'https://faculty.jnu.edu.cn' + faculty_dict['headerPic']
        try:
            img = request.urlretrieve(img_url, img_path + name + '.jpg')
        except error.HTTPError as e:
            print(e)
    tds = random.randint(1, 10)
    time.sleep(tds / 10)
