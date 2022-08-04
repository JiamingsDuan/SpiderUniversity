import random
import requests
import json
import time
import math
import os
from tqdm import tqdm

from mongodb_database import MongoDB

num = 2804
subject = "T"

base_url = 'https://c.wanfangdata.com.cn/Category/Magazine/search'
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'content-length': '306',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://c.wanfangdata.com.cn',
    'referer': 'https://c.wanfangdata.com.cn/periodical?class_code=' + subject,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55',
}

base_img_url = 'https://www.wanfangdata.com.cn/images/PeriodicalImages/'
save_path = './wanfang_journals/' + subject + '/json/'
img_path = './wanfang_journals/' + subject + '/img/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(save_path)
make_dir(img_path)
for i in range(math.ceil(num / 100)):

    bit = random.randint(0, 10)
    digit = random.randint(0, 10)
    waiting = bit + digit / 10
    time.sleep(waiting)

    json_data = {
        "query": [],
        "start": 100 * i,
        "rows": 100,
        "sort_field": {"sort_field": "LastYear;HasFulltext;CoreScore"},
        "highlight_field": "",
        "pinyin_title": [],
        "class_code": subject,
        "core_periodical": [],
        "sponsor_region": [],
        "publishing_period": [],
        "publish_status": "",
        "return_fields": ['Address',
                          'ArticleAvgDownload',
                          'ArticleNo',
                          'Award',
                          'CN',
                          'Chief',
                          'ChiefEditor',
                          'CitedCount',
                          'ClassCode',
                          'CompetentDepartment',
                          'CorePeriodical',
                          'CorePeriodicalYear',
                          'Director',
                          'DownloadCount',
                          'Editorial',
                          'Email',
                          'Fax',
                          'FormerTitle',
                          'FoundYear',
                          'FundArticleCount',
                          'HighLight',
                          'ISSN',
                          'Id',
                          'ImpactFactor',
                          'Initial',
                          'Introduction',
                          'IsPrePublished',
                          'IsStopped',
                          'IssuedPeriod',
                          'Language',
                          'LastIssue',
                          'LastYear',
                          'Postcode',
                          'PrimeColumn',
                          'ResourceType',
                          'Sponsor',
                          'SponsorRegion',
                          'Telephone',
                          'Title',
                          'Url',
                          'YearIssue', ]
    }

    response = requests.post(url=base_url, data=json.dumps(json_data), headers=headers)
    contents = response.json()
    # print(contents['value'][0]['Title'][0])
    for journal_info_dict in tqdm(contents['value']):
        journal_info_json = json.dumps(journal_info_dict, ensure_ascii=False, indent=4)
        journal_id = journal_info_dict['Id']
        journal_title = journal_info_dict['Title'][0].replace('/', '_')
        # save to local
        db = MongoDB(host='localhost', db='PaperBox')
        # 插入操作
        rep = db.insert_one('mdb_sfm_journal_info_wanf_2022', journal_info_dict)
        time.sleep(0.1)
