import json
import os
import requests
from urllib import request, error
from urllib.parse import urlencode


save_path = 'json/'
img_path = 'img/'
col_path = 'col/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(save_path)
make_dir(img_path)
make_dir(col_path)

base_url = 'https://my.nankai.edu.cn/_wp3services/generalQuery?'
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '735',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'my.nankai.edu.cn',
    'Origin': 'https://my.nankai.edu.cn',
    'Referer': 'https://my.nankai.edu.cn/jsflcx/list.htm',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'X-Requested-With': 'XMLHttpRequest',
}
payload = {
    'queryObj': 'teacherHome',
}
form_data = {
    'siteId': 2,
    'pageIndex': 1,
    'rows': 12,
    'returnInfos': [{"field": "collegeId", "name": "collegeId"},
                    {"field": "collegeName", "pattern": [{"name": "lp", "value": 10}], "name": "collegeName"},
                    {"field": "collegeEnName", "name": "collegeEnName"}, {"field": "url", "name": "url"},
                    {"field": "count", "name": "count"}, {"field": "fullDepartName", "name": "fullDepartName"},
                    {"field": "departCategoryId", "name": "departCategoryId"}],
    'articleType': 0,
    'isShowDepart': 0,
    'isDepartUrl': 0,
    'departmentSearch': 1,
    'parentDepartId': 0,
    'departCateShow': 0,
}

url = base_url + urlencode(payload)
response = requests.post(url=url, data=urlencode(form_data), headers=headers)
print(response.status_code)
contents = response.json()['data']
for college_index in range(len(contents)):
    college_dict = contents[college_index]
    name = college_dict['collegeName'].replace(' ', '')
    faculty_info_json = json.dumps(college_dict, indent=4, ensure_ascii=False)
    with open(col_path + name + '.json', 'w', encoding='utf-8') as fo:
        fo.write(faculty_info_json)
        fo.close()
