import json
import os
import random
import time
import requests
import simplejson
from urllib import error, request
from urllib.parse import urlencode

from tqdm import tqdm

save_path = './teacherData/复旦fdu/json/'
img_path = './teacherData/复旦fdu/img/'
col_path = './teacherData/复旦fdu/col/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(save_path)
make_dir(img_path)
make_dir(col_path)

base_url = 'https://faculty.fudan.edu.cn/system/resource/tsites/advancesearch.jsp?'
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'referer': 'https://faculty.fudan.edu.cn/jssyx.jsp?urltype=tree.TreeTempUrl&wbtreeid=1015',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'x-requested-with': 'XMLHttpRequest',
}

for page_index in range(2, 28):
    tds = random.randint(1, 10)
    time.sleep(tds / 10)
    payload = {
        'collegeid': 0,
        'disciplineid': 0,
        'enrollid': 0,
        'pageindex': page_index + 1,
        'pagesize': 12,
        'rankid': 0,
        'degreeid': 0,
        'honorid': 0,
        'pinyin': '',
        'profilelen': 100,
        'teacherName': '',
        'searchDirection': '',
        'viewmode': 8,
        'viewid': 208030,
        'siteOwner': 1542332840,
        'viewUniqueId': 'u9',
        'showlang': 'zh_CN',
        'ispreview': 'false',
        'ellipsis': '',
        'alignright': 'false',
        'productType': 0,
    }
    url = base_url + urlencode(payload)
    print(url)
    response = requests.get(url=url, headers=headers)
    response = response.content.decode('utf-8')
    contents = simplejson.loads(response)

    for teacher_info in tqdm(contents['teacherData']):
        name = teacher_info['name']
        teacher_info_json = json.dumps(teacher_info, indent=4, ensure_ascii=False)
        with open(save_path + name + '.json', 'w', encoding='utf-8') as f:
            f.write(teacher_info_json)
        img_url = 'https://faculty.fudan.edu.cn/' + teacher_info['picUrl']
        try:
            img = request.urlretrieve(img_url, img_path + teacher_info['name'] + '.jpg')
        except error.HTTPError as e:
            pass
        tds = random.randint(1, 10)
        time.sleep(tds / 10)
