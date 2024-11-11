import json
import time
import random
from urllib import request, error
from urllib.parse import urlencode
import requests
import simplejson
from tqdm import tqdm

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
    'Host': 'faculty.dlut.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43',
    'X-Requested-With': 'XMLHttpRequest'
}
save_path = 'json/'
img_path = 'img/'
Base_url = 'http://faculty.dlut.edu.cn/system/resource/tsites/advancesearch.jsp?'

for page_index in range(349, 365):
    print(page_index)
    tds = random.randint(1, 10)
    time.sleep(tds / 10)
    payload = {
        'collegeid': 0,
        'disciplineid': 0,
        'enrollid': 0,
        'pageindex': page_index,
        'pagesize': 9,
        'rankid': 0,
        'degreeid': 0,
        'honorid': 0,
        'pinyin': '',
        'profilelen': 2000,
        'teacherName': '',
        'searchDirection': '',
        'viewmode': 8,
        'viewid': 362222,
        'siteOwner': 1272769371,
        'viewUniqueId': 'u8',
        'showlang': 'zh_CN',
        'ispreview': 'false',
        'basenum': 0,
        'ellipsis': '...',
        'alignright': 'false',
        'productType': 0,
        'tutorType': '',
    }

    url = Base_url + urlencode(payload)
    response = requests.get(url=url, headers=headers)
    contents = response.json()
    # print(contents)
    for teacher_info in tqdm(contents['teacherData']):
        name = teacher_info['name']
        teacher_info_json = json.dumps(teacher_info, indent=4, ensure_ascii=False)
        with open(save_path + name + '.json', 'w', encoding='utf-8') as f:
            f.write(teacher_info_json)
        img_url = 'http://faculty.dlut.edu.cn/' + teacher_info['picUrl']
        try:
            img = request.urlretrieve(img_url, img_path + teacher_info['name'] + '.jpg')
        except error.HTTPError as e:
            pass
        tds = random.randint(1, 10)
        time.sleep(tds / 10)
