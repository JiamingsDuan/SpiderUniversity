import json
import time
import random
from urllib import request, error
from urllib.parse import urlencode
from mongodb_database import MongoDB
import requests
import simplejson
from tqdm import tqdm

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
    'Host': 'homepage.hit.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43',
    'X-Requested-With': 'XMLHttpRequest'
}
save_path = 'json/'
img_path = 'img/'
Base_url = 'http://homepage.hit.edu.cn/sysBrowseShow/executeBrowseAllOfSchoolDepart.do'
url = 'http://homepage.hit.edu.cn/sysBrowseShow/getUserInfoByDeptId.do'
payload = {
    'id': 1,
}

response = requests.post(url=Base_url, data=payload, headers=headers)
# print(response.text)
contents = simplejson.loads(response.text)['list']
college_list = []
for college in contents:
    print(college['deptname'])
    college_list.append(college['id'])
    if college['value'] > 100:
        payloads = {
            'deptId': college['id'],
            'id': 1,
        }
        response_ = requests.post(url=url, data=payloads, headers=headers)
        contents_ = response_.json()
        for sec_dict in contents_['list']:
            name = sec_dict['userName']
            teacher_info_json = json.dumps(sec_dict, indent=4, ensure_ascii=False)
            with open(save_path + name.replace('\n', '') + '.json', 'w', encoding='utf-8') as f:
                f.write(teacher_info_json)

