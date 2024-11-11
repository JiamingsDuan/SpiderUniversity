import random
import time
import requests
import json
import os
from urllib.parse import urlencode
from urllib import request, error
from tqdm import tqdm

college_id = 7
college_title = '外语学院'
save_path = 'json/'
img_path = 'img/'
col_path = 'col/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(save_path)
make_dir(img_path)
make_dir(col_path)
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '785',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'JSESSIONID=222A97BB666B9F8B45256F22C24C2B8F; language=; '
              'BIGipServerpool_172.20.3.202_80=3389199532.20480.0000',
    'Host': 'faculty.ecnu.edu.cn',
    'Origin': 'https://faculty.ecnu.edu.cn',
    'Referer': 'https://faculty.ecnu.edu.cn/_s2/bmlb/list.psp',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'X-Requested-With': 'XMLHttpRequest',
}
# base_url = 'https://faculty.ecnu.edu.cn/_wp3services/generalQuery?'
# payload = {
#     'queryObj': 'teacherHome',
#     't': '0.2840057868669016',
# }
# form_data = {
#     'siteId': 2,
#     'pageIndex': 1,
#     'rows': 100,
#     'returnInfos': [{"field": "collegeId", "name": "collegeId"},
#                     {"field": "collegeName", "pattern": [{"name": "lp", "value": "10"}], "name": "collegeName"},
#                     {"field": "collegeEnName", "name": "collegeEnName"}, {"field": "url", "name": "url"},
#                     {"field": "count", "name": "count"}, {"field": "fullDepartName", "name": "fullDepartName"},
#                     {"field": "departCategoryId", "name": "departCategoryId"},
#                     {"field": "orgType", "name": "orgType"}],
#     'articleType': 0,
#     'isShowDepart': 0,
#     'isDepartUrl': 0,
#     'departmentSearch': 1,
#     'parentDepartId': 0,
#     'orgClassification': 1,
# }

# response = requests.post(url=base_url + urlencode(payload), headers=headers, data=urlencode(form_data))
# contents = response.json()['data']
# name_list = os.listdir(col_path)
# for file_name in name_list:
#     with open(col_path + file_name, 'r', encoding='UTF-8') as f:
#         load_dict = json.load(f)
#         college_id = load_dict['collegeId']
#         college_title = load_dict['collegeName'].split('（')[0]
#         print(college_id, college_title)
# print(college['collegeName'], college['collegeId'])
# college_info_json = json.dumps(college, indent=4, ensure_ascii=False)
# with open(col_path + college['collegeName'].split('（')[0] + '.json', 'w', encoding='utf-8') as f:
#     f.write(college_info_json)
faculty_data = {
    'siteId': str(college_id),
    'pageIndex': 1,
    'rows': 999,
    'conditions': [{"field": "language", "value": "1", "judge": "="},
                   {"field": "title", "value": "", "judge": "like"},
                   {"field": "published", "value": "1", "judge": "="}, {
                       "orConditions": [{"field": "ownDepartment", "value": str(college_id), "judge": "="},
                                        {"field": "exField3",
                                         "value": college_title,
                                         "judge": "="}]}],
    'orders': '',
    'returnInfos': [{"field": "title", "name": "title"},
                    {"field": "career", "name": "career"},
                    {"field": "visitCount", "name": "visitCount"},
                    {"field": "headerPic", "name": "headerPic"},
                    {"field": "cnUrl", "name": "cnUrl"},
                    {"field": "exField3", "name": "exField3"},
                    {"field": "publishStatus", "name": "publishStatus"}],
    'articleType': 1,
    'level': 0,
    'deptTecOrder': '1_1',
    'pageEvent': 'dataSearchByPageIndex',
}
faculty_url = 'https://faculty.ecnu.edu.cn/_wp3services/generalQuery?'
faculty_payload = {
    'queryObj': 'teacherHome',
    't': '0.7148211310030766',
}
faculty_response = requests.post(url=faculty_url + urlencode(faculty_payload), headers=headers, data=faculty_data)
faculty_contents = faculty_response.json()['data']
print(len(faculty_contents))
for faculty_index in tqdm(range(len(faculty_contents) - 1, -1, -1)):
    faculty_dict = faculty_contents[faculty_index]
    name = faculty_dict['title'].replace(' ', '').replace('*', '_')
    faculty_info_json = json.dumps(faculty_dict, indent=4, ensure_ascii=False)
    with open(save_path + name + '.json', 'w', encoding='utf-8') as fo:
        fo.write(faculty_info_json)
        fo.close()
    img_url = 'https://faculty.ecnu.edu.cn' + faculty_dict['headerPic']
    try:
        img = request.urlretrieve(img_url, img_path + name + '.jpg')
    except error.HTTPError as e:
        print(e)
        tds = random.randint(1, 10)
        time.sleep(tds / 10)
