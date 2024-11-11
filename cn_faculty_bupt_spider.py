import json
import random
import time
import requests
import simplejson
from urllib import request, error
from urllib.parse import urlencode
from tqdm import tqdm

save_path = 'json/'
img_path = 'img/'
Base_url = 'https://teacher.bupt.edu.cn/system/resource/tsites/advancesearch.jsp?'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62 ',
    'x-requested-with': 'XMLHttpRequest',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'content-type': 'text/html;charset=UTF-8',
}
for page_index in range(2, 77):
    payload = {
        'collegeid': 0,
        'disciplineid': 0,
        'enrollid': 0,
        'pageindex': page_index,
        'pagesize': 6,
        'rankid': 0,
        'honorid': 0,
        'pinyin': '',
        'profilelen': 100,
        'teacherName': '',
        'searchDirection': '',
        'viewmode': 8,
        'viewid': '133669',
        'siteOwner': '1447934445',
        'viewUniqueId': 'u12',
        'showlang': 'zh_CN',
        'ellipsis': '',
        'alignright': 'false',
        'productType': 0,
    }

    url = Base_url + urlencode(payload)
    response = requests.get(url=url, headers=headers)
    response = response.content.decode('utf-8')
    contents = simplejson.loads(response)
    print(type(contents))
    for teacher_info in tqdm(contents['teacherData']):
        name = teacher_info['name']
        teacher_info_json = json.dumps(teacher_info, indent=4, ensure_ascii=False)
        with open(save_path + name + '.json', 'w', encoding='utf-8') as f:
            f.write(teacher_info_json)
        img_url = 'https://teacher.bupt.edu.cn/' + teacher_info['picUrl']
        try:
            img = request.urlretrieve(img_url, img_path + teacher_info['name'] + '.jpg')
            # print(journal_info['Title'][0] + '-> save success')
        except error.HTTPError as e:
            # print(e.code)
            pass
        tds = random.randint(1, 10)
        time.sleep(tds / 10)
