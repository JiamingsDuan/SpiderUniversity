import json
import time
import random
from urllib import request, error
from urllib.parse import urlencode
import requests
import simplejson
from lxml import etree
from tqdm import tqdm

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
    'Host': 'faculty.uestc.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43',
    'X-Requested-With': 'XMLHttpRequest'
}
save_path = 'json/'
img_path = 'img/'

# for page_index in range(115, 152):
#     print(page_index)
#     tds = random.randint(0, 5)
#     time.sleep(tds + tds / 10)
#     payload = {
#         'collegeid': 0,
#         'disciplineid': 0,
#         'enrollid': 0,
#         'pageindex': page_index + 1,
#         'pagesize': 16,
#         'rankid': 0,
#         'degreeid': 0,
#         'honorid': 0,
#         'pinyin': '',
#         'profilelen': 100,
#         'teacherName': '',
#         'searchDirection': '',
#         'viewmode': 8,
#         'viewid': '225569',
#         'siteOwner': '1362264394',
#         'viewUniqueId': '225569',
#         'showlang': 'zh_CN',
#         'ispreview': 'false',
#         'ellipsis': '',
#         'alignright': 'false',
#         'productType': 0,
#     }
#
#     url = Base_url + urlencode(payload)
#     response = requests.get(url=url, headers=headers)
#     response = response.content.decode('utf-8')
#     contents = simplejson.loads(response)
#     for teacher_info in tqdm(contents['teacherData']):
#         name = teacher_info['name']
#         teacher_info_json = json.dumps(teacher_info, indent=4, ensure_ascii=False)
#
#         with open(save_path + name + '.json', 'w', encoding='utf-8') as f:
#             f.write(teacher_info_json)
#         img_url = 'https://faculty.uestc.edu.cn/' + teacher_info['picUrl']
#         try:
#             img = request.urlretrieve(img_url, img_path + teacher_info['name'] + '.jpg')
#         except error.HTTPError as e:
#             pass
#         tds = random.randint(1, 10)
#         time.sleep(tds / 10)
college_url = 'https://faculty.uestc.edu.cn/xylb.jsp?'

college_payload = {
    'urltype': 'tsites.CollegeTeacherList',
    'wbtreeid': 1021,
    'st': 0,
    'id': 2037,
    'lang': 'zh_CN',
}
response = requests.get(url=college_url + urlencode(college_payload), headers=headers)
dom = etree.HTML(response.text)
college_url = dom.xpath('*//ul[@class="yiji"]/li/a/href()')
college_name = dom.xpath('*//ul[@class="yiji"]/li/a/p/text()')
print(college_url)
