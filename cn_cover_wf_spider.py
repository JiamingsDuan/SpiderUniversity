import requests
import json
import simplejson
import math
from pymongo import MongoClient
from tqdm import tqdm

base_dir = 'images_wanfang/'
headers = {
    'host': 'c.wanfangdata.com.cn',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29 ',
    'origin': 'https://c.wanfangdata.com.cn',
    'referer': 'https://c.wanfangdata.com.cn/periodical?class_code=B',
}

count = 1959
code_list = []
subject = "G"
"""
B,C,F,G,N,R,S,T
"""


class MongoDB:
    def __init__(self, host, db, port=27017):
        """
        :param host: str mongodb地址
        :param db: str 数据库
        :param port: int 端口，默认为27017
        """
        host = host
        db = db
        self.port = port
        client = MongoClient(host=host, port=port)
        self.db = client[db]

    def insert_one(self, table, dic):
        """
        :param table: str 数据库中的集合
        :param dic: dict 要插入的字典
        :return: 返回一个包含ObjectId类型的对象
        """
        collecting = self.db[table]
        response = collecting.insert_one(dic)

        return response


base_url = 'https://c.wanfangdata.com.cn/Category/Magazine/search'

for i in range(0, math.ceil(count / 100)):
    json_data = {
        "query": [],
        "start": 0 + i * 100,
        "rows": 100,
        "sort_field": {
            "sort_field": "ImpactFactor"
        },
        "highlight_field": "",
        "pinyin_title": [],
        "class_code": subject,
        "core_periodical": [],
        "sponsor_region": [],
        "publishing_period": [],
        "publish_status": "",
        "return_fields": [
            'Id',
            'fxyj',
            'Title',
            'Language',
            'FormerTitle',
            'Address',
            'Postcode',
            'Url',
            'Telephone',
            'Email',
            'Fax',
            'ISSN',
            'CN',
            'LastYear',
            'LastIssue',
            'YearIssue',
            'Introduction',
            'ClassCode',
            'Editorial',
            'Award',
            'PrimeColumn',
            'Sponsor',
            'SponsorRegion',
            'CompetentDepartment',
            'Director',
            'Chief',
            'ChiefEditor',
            'CorePeriodical',
            'ImpactFactor',
            'ArticleNo',
            'DownloadCount',
            'CitedCount',
            'ArticleAvgDownload',
            'Initial',
            'IssuedPeriod',
            'FoundYear',
            'IsStopped',
            'IsPrePublished',
            'FundArticleCount',
            'CorePeriodicalYear',
            'HighLight',
            'ResourceType'
        ]
    }
    data = json.dumps(json_data)
    html = requests.post(url=base_url, data=data, headers=headers)
    html_str = html.content.decode('utf-8')
    contents = simplejson.loads(html_str)

    for journal_info in tqdm(contents['value']):
        journal_info['CN_Title'] = journal_info['Title'][0]
        # journal_info['EN_Title'] = journal_info['Title'][1]
        db = MongoDB(host='localhost', db='test')
        # 插入操作
        rep = db.insert_one('WanFang_journal_information', journal_info)
        # image_url = 'https://www.wanfangdata.com.cn/images/PeriodicalImages/' \
        #             + journal_info['Id'] + '/' + journal_info['Id'] + '.jpg '
        # print(image_url)
        # img = requests.get(image_url)
        # f = open(base_dir + journal_info['Title'][0] + '.jpg', 'ab')
        # f.write(img.content)  # 多媒体存储content
        # f.close()
        print(journal_info['Title'][0])
