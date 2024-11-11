import random
import time
import requests
import json
import random
import simplejson
from mongodb_database import MongoDB
from tqdm import tqdm
from urllib.parse import urlencode

save_path = '../json_major/'
base_url = 'https://api.eol.cn/gkcx/api/?'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://gkcx.eol.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29 '
}


for page in range(1, 142):
    json_data = {
        "access_token": "",
        "admissions": "",
        "central": "",
        "department": "",
        "dual_class": "",
        "f211": "",
        "f985": "",
        "is_doublehigh": "",
        "is_dual_class": "",
        "keyword": "",
        "nature": "",
        "page": page,
        "province_id": "",
        "ranktype": "",
        "request_type": 1,
        "school_type": "",
        "size": 20,
        "sort": "",
        "top_school_id": "",
        "type": "",
        "uri": "apidata/api/gk/school/lists"
    }

    urls = base_url + urlencode(json_data)
    html = requests.post(url=urls, headers=headers)
    html_str = html.content.decode('utf-8')
    contents = simplejson.loads(html_str)
    # print(contents)
    tg = random.randint(5, 7)
    td = random.randint(1, 10)
    time.sleep(tg + td / 10)

    for item in tqdm(contents['data']['item']):
        code = item['school_id']
        name = item['name']
        # print(name, code)

        # 基本信息
        # university_url = 'https://static-data.eol.cn/www/2.0/school/' + str(code) + '/info.json'
        # university_file = requests.get(url=university_url, headers=headers)
        # university_data_info = university_file.content.decode('utf-8')  # str
        # university_contents = simplejson.loads(university_data_info)
        # university_information_dict = university_contents['data']
        # university_info_json = json.dumps(university_information_dict, indent=4, ensure_ascii=False)
        # with open(save_path + name + '.json', 'w', encoding='utf-8') as f:
        #     f.write(university_info_json)
        # db = MongoDB(host='localhost', db='test')
        # rep = db.insert_one('cn_university_full_information', university_information_dict)

        # 专业信息
        major_url = 'https://static-data.eol.cn/www/2.0/school/' + str(code) + '/pc_special.json'
        major_file = requests.get(url=major_url, headers=headers)
        major_data_info = major_file.content.decode('utf-8')  # str
        major_contents = simplejson.loads(major_data_info)
        major_information_dict = major_contents['data']
        major_info_json = json.dumps(major_information_dict, indent=4, ensure_ascii=False)
        with open(save_path + name + '.json', 'w', encoding='utf-8') as f:
            f.write(major_info_json)
        tds = random.randint(1, 10)
        time.sleep(tds / 10)
