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
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=A90FE765612C364A7131657B41F8BB84',
    'Host': 'faculty.scu.edu.cn',
    'Referer': 'http://faculty.scu.edu.cn/jscx.jsp?urltype=tree.TreeTempUrl&wbtreeid=1013',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'X-Requested-With': 'XMLHttpRequest',
}

base_url = 'http://faculty.scu.edu.cn/system/resource/tsites/advancesearch.jsp?'
for page_index in range(31):
    payload = {
        'collegeid': 0,
        'disciplineid': 0,
        'enrollid': 0,
        'pageindex': page_index + 1,
        'pagesize': 16,
        'rankid': 0,
        'degreeid': 0,
        'honorid': 0,
        'pinyin': '',
        'profilelen': 100,
        'teacherName': '',
        'searchDirection': '',
        'viewmode': 10,
        'viewid': '382740',
        'siteOwner': '1635361356',
        'viewUniqueId': '382740',
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
        img_url = 'http://faculty.scu.edu.cn' + faculty_dict['picUrl']
        try:
            img = request.urlretrieve(img_url, img_path + name + '.jpg')
        except error.HTTPError as e:
            print(e)
    tds = random.randint(1, 10)
    time.sleep(tds / 10)
