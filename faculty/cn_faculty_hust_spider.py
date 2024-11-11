import os
import json
import time
import random
from urllib import request, error
from urllib.parse import urlencode
import requests
import simplejson
from tqdm import tqdm
from lxml import etree

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
    'Host': 'faculty.hust.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'text/html;charset=UTF-8',
}
save_path = 'json/'
img_path = 'img/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(save_path)
make_dir(img_path)

college_payload = {
    'urltype': 'tree.TreeTempUrl',
    'wbtreeid': '1023',
    'action': 'college',
    'fcode': '',
    'showlang': 'zh_CN',
    'showtype': 0,
}
college_url = 'http://faculty.hust.edu.cn/sjy.jsp?' + urlencode(college_payload)
teacher_url = 'http://faculty.hust.edu.cn/system/resource/tsites/asy/asyqueryteacher.jsp?'


def fetch_college_information():
    college_response = requests.get(url=college_url, headers=headers)
    college_response = college_response.content.decode('utf-8')
    college_str = college_response.split('sites$$')[1].split('$$')[0].replace('},{', '} {').replace('[', '').replace(
        ']', '')
    college_list = college_str.split(' ')
    college_code_list = []
    for college in college_list:
        college_dict = simplejson.loads(college)
        content_json = json.dumps(college_dict, indent=4, ensure_ascii=False)
        with open(col_path + college_dict['collegeName'] + '.json', 'w', encoding='utf-8') as f:
            f.write(content_json)
        college_code_list.append(college_dict['collegeId'])
    return college_code_list


# for page_index in range(0, 1):
#     teacher_payload = {
#         'collegeid': 2373,
#         'disciplineid': 0,
#         'pageindex': page_index + 1,
#         'pagesize': 8,
#         'rankid': 0,
#         'honorid': 0,
#         'py': '',
#         'viewmode': 8,
#         'viewid': 66517,
#         'siteOwner': 1391599222,
#         'viewUniqueId': 66517,
#         'showlang': '',
#         'type': 'collgeteacher',
#     }
#     url = teacher_url + urlencode(teacher_payload)
#     response = requests.get(url=url, headers=headers)
#     response = response.content.decode('utf-8')
#     contents = simplejson.loads(response)
#     for teacher_info in tqdm(contents['teacherData']):
#         name = teacher_info['name']
#         teacher_info['collegeid'] = teacher_payload['collegeid']
#         teacher_info_json = json.dumps(teacher_info, indent=4, ensure_ascii=False)
#         with open(save_path + name + '.json', 'w', encoding='utf-8') as f:
#             f.write(teacher_info_json)
#         img_url = 'https://faculty.hust.edu.cn/' + teacher_info['picUrl']
#         try:
#             img = request.urlretrieve(img_url, img_path + teacher_info['name'] + '.jpg')
#         except error.HTTPError as e:
#             pass
name_list = os.listdir(save_path)
for i in range(688, len(name_list)):
    with open(save_path + name_list[i], 'r', encoding='UTF-8') as f:
        load_dict = json.load(f)
        img_url = 'http://faculty.hust.edu.cn/' + load_dict['picUrl']
        try:
            img = request.urlretrieve(img_url, img_path + load_dict['name'] + '.jpg')
        except error.HTTPError as e:
            pass
