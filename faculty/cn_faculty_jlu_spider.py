import json
import time
import random
from urllib import request, error
from urllib.parse import urlencode
from mongodb_database import MongoDB
import requests
import simplejson
from tqdm import tqdm
import urllib3
urllib3.disable_warnings()

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43',
    'X-Requested-With': 'XMLHttpRequest',
    'Host': 'teachers.jlu.edu.cn',
}
save_path = 'json/'
img_path = 'img/'
Base_url = 'https://teachers.jlu.edu.cn/system/resource/tsites/advancesearch.jsp?'

for page_index in range(170, 177):
    payload = {
        'collegeid': 0,
        'disciplineid': 0,
        'enrollid': 0,
        'pageindex': page_index,
        'pagesize': 10,
        'rankid': 0,
        'honorid': 0,
        'pinyin': '',
        'profilelen': 100,
        'teacherName': '',
        'searchDirection': '',
        'viewmode': 8,
        'viewid': 137576,
        'siteOwner': 1404698814,
        'viewUniqueId': 'u11',
        'showlang': 'zh_CN',
        'ispreview': 'false',
        'ellipsis': '...',
        'alignright': 'false',
        'productType': 0,
    }

    url = Base_url + urlencode(payload)
    # print(url)
    response = requests.get(url=url, headers=headers, verify=False)
    contents = simplejson.loads(response.text)

    for teacher_info in tqdm(contents['teacherData']):
        # print(teacher_info)
        name = teacher_info['name']
        teacher_info_json = json.dumps(teacher_info, indent=4, ensure_ascii=False)
        # db = MongoDB(host='localhost', db='test')
        # rep = db.insert_one('mdb_sfm_teacherData_dlut', teacher_info)
        with open(save_path + name.replace('\n', '') + '.json', 'w', encoding='utf-8') as f:
            f.write(teacher_info_json)
        img_url = 'https://teachers.jlu.edu.cn/' + teacher_info['picUrl']
        # try:
        #     img = request.urlretrieve(img_url, img_path + teacher_info['name'].replace('\n', '') + '.jpg')
        #     # print(journal_info['Title'][0] + '-> save success')
        # except error.HTTPError as e:
        #     # print(e.code)
        #     pass
        tds = random.randint(1, 10)
        time.sleep(tds / 10)
