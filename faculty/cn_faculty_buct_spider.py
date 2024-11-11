import json
import os
import requests
from urllib import request, error
from urllib.parse import urlencode
from tqdm import tqdm

save_path = 'json/'
img_path = 'img/'
col_path = 'col/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(save_path)
make_dir(img_path)
make_dir(col_path)

name_list = os.listdir(col_path)
for file_name in name_list:
    with open(col_path + file_name, 'r', encoding='UTF-8') as f:
        load_dict = json.load(f)
        code = load_dict['collegeId']
        college_id = code

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-length': '962',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'JSESSIONID=340AE7ED92E74E651839F70F223E20FB; language=',
        'origin': 'https://faculty.buct.edu.cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
        'x-requested-with': 'XMLHttpRequest',
    }
    Base_url = 'https://faculty.buct.edu.cn/_wp3services/generalQuery?'
    payload = {
        'queryObj': 'teacherHome',
        't': '0.37036209162427336',
    }
    url = Base_url + urlencode(payload)
    form_data = {
        'siteId': college_id,
        'pageIndex': 1,
        'rows': 52,
        'conditions': [{"field": "language", "value": "1", "judge": "="},
                       {"field": "ownDepartment", "value": str(college_id), "judge": "="},
                       {"field": "title", "value": "", "judge": "like"},
                       {"field": "published", "value": "1", "judge": "="}],
        'orders': '',
        'returnInfos': [{"field": "title", "name": "title"}, {"field": "career", "name": "career"},
                        {"field": "visitCount", "name": "visitCount"}, {"field": "headerPic", "name": "headerPic"},
                        {"field": "cnUrl", "name": "cnUrl"}, {"field": "department", "name": "department"},
                        {"field": "publishStatus", "name": "publishStatus"}],
        'articleType': 1,
        'level': 0,
        'deptTecOrder': '1_1',
        'pageEvent': 'dataSearchByPageIndex',
    }

    response = requests.post(url=url, data=urlencode(form_data), headers=headers)
    contents = response.json()['data']
    # print(contents[0]['title'])
    for faculty_dict in tqdm(contents):
        title = faculty_dict['title']
        teacher_info_json = json.dumps(faculty_dict, indent=4, ensure_ascii=False)
        with open(save_path + title + '.json', 'w', encoding='utf-8') as f:
            f.write(teacher_info_json)
        img_url = 'https://faculty.buct.edu.cn' + faculty_dict['headerPic']
        try:
            img = request.urlretrieve(img_url, img_path + faculty_dict['title'] + '.jpg')
        except error.HTTPError as e:
            pass
