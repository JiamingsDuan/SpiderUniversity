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
    'Cookie': 'JSESSIONID=578323F12F640D7A845E5515A0B928D2; BIGipServerpool_192.168.178.148=2494736576.20480.0000',
    'Host': 'faculty.csu.edu.cn',
    'Referer': 'https://faculty.csu.edu.cn/jscx.jsp?urltype=tree.TreeTempUrl&wbtreeid=1004',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 '
                  'Safari/537.36 Edg/96.0.1054.62',
    'X-Requested-With': 'XMLHttpRequest',
}

base_url = 'https://faculty.csu.edu.cn/system/resource/tsites/advancesearch.jsp?'
for page_index in range(109):
    payload = {
        'collegeid': 0,
        'disciplineid': 0,
        'enrollid': 0,
        'pageindex': page_index + 1,
        'pagesize': 20,
        'rankid': 0,
        'degreeid': 0,
        'honorid': 0,
        'pinyin': '',
        'profilelen': 100,
        'teacherName': '',
        'searchDirection': '',
        'viewmode': 8,
        'viewid': '382942',
        'siteOwner': '1252142266',
        'viewUniqueId': '382942',
        'showlang': 'zh_CN',
        'ispreview': 'false',
        'basenum': 0,
        'ellipsis': '...',
        'alignright': 'false',
        'productType': 0,
        'tutorType': '',
    }

    url = base_url + urlencode(payload)
    response = requests.get(url=url, headers=headers)
    contents = response.json()['teacherData']
    for faculty_index in tqdm(range(len(contents))):
        faculty_dict = contents[faculty_index]
        name = faculty_dict['name'].replace(' ', '')
        faculty_info_json = json.dumps(faculty_dict, indent=4, ensure_ascii=False)
        with open(save_path + name + '.json', 'w', encoding='utf-8') as fo:
            fo.write(faculty_info_json)
            fo.close()
        img_url = 'https://faculty.csu.edu.cn' + faculty_dict['picUrl']
        try:
            img = request.urlretrieve(img_url, img_path + name + '.jpg')
        except error.HTTPError as e:
            print(e)
    tds = random.randint(1, 10)
    time.sleep(tds / 10)
